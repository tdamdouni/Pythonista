# https://gist.github.com/omz/5048588

# Simple installer script for using the Evernote SDK in Pythonista
# 
# This script should be run from the root directory. In order to keep things
# tidy, it installs the module and all its dependencies in a directory named
# 'evernote-sdk'. In order to be able to import it, you have to add that to
# your import path, like this:
# 
# import sys
# sys.path.append('evernote-sdk')
# 
# (this assumes that the script is in the root directory.)

import tarfile
import shutil
import urllib
import os

try:
	os.mkdir('evernote-sdk')
except:
	pass

print 'Downloading evernote...'
filename, headers = urllib.urlretrieve('https://pypi.python.org/packages/source/e/evernote/evernote-1.23.2.tar.gz')
print 'Installing evernote...'
t = tarfile.open(filename, 'r')
t.extractall()
t.close()
shutil.move('evernote-1.23.2/lib/evernote', 'evernote-sdk/evernote')
shutil.move('evernote-1.23.2/lib/thrift', 'evernote-sdk/thrift')
shutil.rmtree('evernote-1.23.2')

print 'Downloading httplib2...'
filename, headers = urllib.urlretrieve('https://pypi.python.org/packages/source/h/httplib2/httplib2-0.7.7.tar.gz')
print 'Installing httplib2...'
t = tarfile.open(filename, 'r')
t.extractall()
t.close()
shutil.move('httplib2-0.7.7/python2/httplib2', 'evernote-sdk/httplib2')
shutil.rmtree('httplib2-0.7.7')

print 'Downloading oauth2...'
filename, headers = urllib.urlretrieve('https://pypi.python.org/packages/source/o/oauth2/oauth2-1.5.211.tar.gz')
print 'Installing oauth2...'
t = tarfile.open(filename, 'r')
t.extractall()
t.close()
shutil.move('oauth2-1.5.211/oauth2', 'evernote-sdk/oauth2')
shutil.rmtree('oauth2-1.5.211')

import editor
editor.reload_files()

print 'Done.'