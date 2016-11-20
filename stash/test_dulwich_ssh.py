#!python2

# https://gist.github.com/jsbain/e60abaa38bd5685637e758175d7f2bda

from dulwich.client import (
    get_transport_and_path,
    )
from dulwich.protocol import ZERO_SHA
from dulwich.repo import (BaseRepo, Repo)
import dulwich.client
import os,sys,shutil
import logging
import paramiko
source='ssh://git@github.com/jsbain/uicomponents.git'


#setup logging
logger=logging.getLogger("paramiko")
if logger.handlers:
	logger.removeHandler([logger.handlers[0]])
if not logger.handlers:
	hdlr = logging.FileHandler('paramikolog.txt','w')
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
logger.debug('logging started')



#setup client
dulwich.client.get_ssh_vendor = dulwich.client.ParamikoSSHVendor
def report_activity(siz,action):
	logger.debug('          #{}     {}'.format(siz,action))
client, host_path = get_transport_and_path(source,report_activity=report_activity)

#set up local repo
target=os.path.expanduser('~/Documents/dulwichtests')
if not os.path.exists(target):
	os.mkdir(target)
	r = Repo.init(target)
else:
	#shutil.rmtree(target+'/.git')
	#r = Repo.init(target)
	r=Repo(target)
	
	
def determine_wants( refs):
	print('#### server has these refs ####')
	for (ref,sha) in refs.items():
		print(' {} {}'.format(ref,sha))
	wants= [sha for (ref, sha) in refs.items()
	if not sha in r.object_store and not ref.endswith(b"^{}") and
	not sha == ZERO_SHA]
	print('asking for {}'.format(wants[0]))
	return [wants[0]] #testing: try one at a time
	
def fetch_one():
	remote_refs = client.fetch(host_path, r,
	determine_wants=determine_wants,
	progress=sys.stdout.write)
	
fetch_one()

