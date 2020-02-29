from __future__ import print_function
# https://gist.github.com/mlgill/8310779

import sys, os, re
sys.path += ['lib']
import keychainsetup, github3

# gist_update_batch
# by Michelle L. Gill, michelle@michellelynngill.com

# A script to batch update pythonist scipts. Scripts to be updated must
# have the following the first line formatted as such:
#
# '#GISTINFO id:l2s0kfj0lsdkf93dkf strip:var_1,var_2'
#
# In this line, the variables understood are:
#         id       : (required) the gist id number
#         strip    : (optional) a comma separated list of variables whose values
#                               will be anonymized before uploading
#         gistname : (optional) the filename on GitHub if different from local one

# This script also requires the github3 module (https://github.com/sigmavirus24/github3.py)
# and my keychainsetup script (https://gist.github.com/8310754).

# Change log
# 2013/01/07: initial version

##################################################################
#                                                                #
#                  User specified parameters                     #
#                                                                #
##################################################################

####### REGEX FILTERS NOT WORKING YET #######
# only files which match regexes in this list will be considered
include_list = [r'.+\.py$']

# then files which match regular expressions in this list will be removed
exclude_list = [r'__init__', r'Untitled']

# the dummy string to replace varibles
dummystr = 'xxxxxx'

##################################################################
#                                                                #
#      Probably don't need to change anything below this point   #
#                                                                #
##################################################################

print("""
****************************************
*          Gist Auto Updater           *
****************************************
""")

# get the list of files--may need to change the walk directory if this file is moved
filelist = list()
for root, dirs, fils in os.walk('.'):
	for fil in fils:
		filelist.append(re.sub(r'^[\.\/]+', '', os.sep.join([root,fil])))
		
####### REGEX FILTERS NOT WORKING YET #######
# # keep only the includes
for reg in include_list:
	regc = re.compile(reg)
	filelist = [x for x in filelist if re.search(regc,x)]
	
# # remove the excludes
for reg in exclude_list:
	regc = re.compile(reg)
	filelist = [x for x in filelist if re.search(regc,x) is None]
	
# login to github
username, password = keychainsetup.set_get_user_pass('github')
gh = github3.login(username,password)

# get all gist ids
gistlist = [x for x in gh.iter_gists()]
gistidlist = [x.id for x in gistlist]

# get gist info (ids, variables to strip) and put in a dict
gistattrdict = dict()
for fil in filelist:
	fh = open(fil,'r')
	fl = fh.readline()
	if '#GISTINFO' in fl:
		gistid = re.search(r"""id:(?P<gistid>\w+)""",fl).group('gistid')
		if gistid not in gistidlist:
			print('Gist id %s for file %s not found in your gists.' % (gistid,fil))
		else:
			# get the gist instance
			gist = [y for (x,y) in zip(gistidlist,gistlist) if x==gistid][0]
			
			# get the variables whose values will be stripped
			try:
				striplist = re.search(r"""strip:(?P<strip>[\w,]+)""",fl).group('strip').split(',')
			except:
				striplist = []
				
			# get the short name of the gist
			try:
				gistname = re.search(r"""gistname:(?P<gistname>[\w\.]+)""",fl).group('gistname')
			except:
				gistname = os.path.basename(fil)
				
			# pack all this info into a dict
			gistattrdict[fil] = {'gist':gist, 'name':gistname, 'id':gistid, 'strip':striplist}
			
# update the gists with cleaned files
for fil in gistattrdict.keys():

	# get the file data except for the GISTINFO line
	fh = open(fil,'r')
	filstr = ''.join(fh.readlines()[1:])
	fh.close()
	
	# substitute any sensitive values for a dummy value
	gistattr = gistattrdict[fil]
	for strip in gistattr['strip']:
		filstr = re.sub('(?P<begin>'+strip+'\s*?=\s*?[\'\"])(.+?)(?P<close>[\'\"])', r'\g<begin>' + dummystr + r'\g<close>', filstr)
		
	# update the gist
	gistup = gistattr['gist']
	gistname = gistattr['name']
	success = gistup.edit(files={gistname:{'content':filstr}})
	if success:
		print('Gist %s was succcessfully updated.' % gistname)
	else:
		print('Gist %s was not updated.' % gistname)
		
print('\nGist update is complete.\n')

