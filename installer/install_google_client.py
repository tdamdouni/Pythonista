from __future__ import print_function
# Simple installer script for using the google-api-client in Pythonista
# 
# This script should be run from the root directory. In order to keep things
# tidy, it installs the module and all its dependencies in a directory named
# 'google-api'. In order to be able to import it, you have to add that to
# your import path, like this:
# 
# import sys
# sys.path.append('google-api')
# 
# (this assumes that the script is in the root directory.)
 
import tarfile
import shutil
import urllib
import os
 
try:
	os.mkdir('google-api')
except:
	pass
 
print('Downloading google-api-client...')
filename, headers = urllib.urlretrieve('https://pypi.python.org/packages/source/g/google-api-python-client/google-api-python-client-1.0.tar.gz')
print('Installing google-api-client...')
t = tarfile.open(filename, 'r')
t.extractall()
t.close()
shutil.move('google-api-python-client-1.0/apiclient', 'google-api/apiclient')
shutil.move('google-api-python-client-1.0/oauth2client', 'google-api/oauth2client')
shutil.move('google-api-python-client-1.0/uritemplate', 'google-api/uritemplate')
shutil.rmtree('google-api-python-client-1.0')

print('Downloading python-gflags...')
filename, headers = urllib.urlretrieve('https://pypi.python.org/packages/source/p/python-gflags/python-gflags-2.0.tar.gz')
print('Installing python-gflags...')
t = tarfile.open(filename, 'r')
t.extractall()
t.close()
shutil.move('python-gflags-2.0/gflags.py', 'google-api/gflags.py')
shutil.move('python-gflags-2.0/gflags2man.py', 'google-api/gflags2man.py')
shutil.move('python-gflags-2.0/gflags_validators.py', 'google-api/gflags_validators.py')
shutil.rmtree('python-gflags-2.0')

print('Downloading httplib2...')
filename, headers = urllib.urlretrieve('https://pypi.python.org/packages/source/h/httplib2/httplib2-0.7.7.tar.gz')
print('Installing httplib2...')
t = tarfile.open(filename, 'r')
t.extractall()
t.close()
shutil.move('httplib2-0.7.7/python2/httplib2', 'google-api/httplib2')
shutil.rmtree('httplib2-0.7.7')

import editor
editor.reload_files()
 
print('Done.')
