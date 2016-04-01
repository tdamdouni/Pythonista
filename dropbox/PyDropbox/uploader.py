import os
from dropbox_client import get_client
import pprint
from dropbox_filenames import REMOTE_ROOT

pp = pprint.PrettyPrinter(indent=4)
APP_NAME = 'pet sitting'

OVERWRITE = True

client = get_client(APP_NAME)

def put_files(filenames, local='', remote=''):
    source_basedir = os.path.join(os.path.realpath(os.curdir), local)
    for filename in filenames:
        source_file = os.path.join(source_basedir, filename)
        if file_exists(source_file) is True:
            destination = os.path.join(remote, filename)
            with open(source_file, 'r') as fh:
                print "Uploading file '{source_file}'".format(source_file=source_file)
                result = client.put_file(destination, fh, overwrite=OVERWRITE)
            pp.pprint(result)
        else: 
            print 'File not found: "{0}'.format(source_file)
        
        

def file_exists(filename):
    return os.path.exists(filename)
