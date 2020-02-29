from __future__ import print_function
# Install SimPy

import urllib
import tarfile
import shutil
import console
import os

name = 'sympy'
version = '0.7.5'

# It is easy to install any pypi pure python package, for example:
# name = 'simpy'
# version = '3.0.2'

fullname = name+'-'+version

print('Downloading '+name+'...')
url = 'https://pypi.python.org/packages/source/s/'+name+'/'+fullname+'.tar.gz'
urllib.urlretrieve(url, 'packget.tar.gz')

print('Extracting...')
t = tarfile.open('packget.tar.gz')
t.extractall()
if os.path.isdir(name):
	shutil.rmtree(name)
shutil.move(fullname+'/'+name, './'+name)

print('Cleaning up...')
shutil.rmtree(fullname)
os.remove('packget.tar.gz')
print('Done.')
