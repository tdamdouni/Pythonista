from __future__ import print_function
# [Other ways to convert Markdown/HTML to PDF in iOS](https://omz-forums.appspot.com/editorial/post/5880187380039680)

# python script I used to install everything (I have a directory 'Scripts' that contains all python stuff):

import urllib
import tarfile
from zipfile import ZipFile
import shutil
import console
import os
import editor
from os.path import expanduser

os.chdir(expanduser('~/Documents/'))

url = 'http://www.reportlab.com/ftp/reportlab-2.7.tar.gz'
fname='reportlab-2.7'
sname='src/reportlab'
dname='Scripts/reportlab'
print('Downloading '+dname+'...')
urllib.urlretrieve(url, fname+'.tar.gz')

print('Extracting...')
t = tarfile.open(fname+'.tar.gz')
t.extractall()

if os.path.isdir(dname):
	shutil.rmtree(dname)
shutil.move(fname+'/'+sname, dname)

print('Cleaning up...')
shutil.rmtree(fname)
os.remove(fname+'.tar.gz')

url='http://pybrary.net/pyPdf/pyPdf-1.13.tar.gz'
fname='pyPdf-1.13'
sname='pyPdf'
dname='Scripts/pyPdf'
print('Downloading '+dname+'...')
urllib.urlretrieve(url, fname+'.tar.gz')

print('Extracting...')
t = tarfile.open(fname+'.tar.gz')
t.extractall()

if os.path.isdir(dname):
	shutil.rmtree(dname)
shutil.move(fname+'/'+sname, dname)

print('Cleaning up...')
shutil.rmtree(fname)
os.remove(fname+'.tar.gz')


url = 'https://github.com/html5lib/html5lib-python/archive/master.zip'
fname='html5lib-python-master'
sname='html5lib'
dname='Scripts/html5lib'
print('Downloading '+dname+'...')
urllib.urlretrieve(url, fname+'.zip')

print('Extracting...')
with ZipFile(fname+'.zip', 'r') as z:
	z.extractall()
	
if os.path.isdir(dname):
	shutil.rmtree(dname)
shutil.move(fname+'/'+sname, dname)

print('Cleaning up...')
shutil.rmtree(fname)
os.remove(fname+'.zip')

url='https://github.com/chrisglass/xhtml2pdf/archive/master.zip'
fname='xhtml2pdf-master'
sname='xhtml2pdf'
dname='Scripts/xhtml2pdf'
print('Downloading '+dname+'...')
urllib.urlretrieve(url, fname+'.zip')

print('Extracting...')
with ZipFile(fname+'.zip', 'r') as z:
	z.extractall()
	
if os.path.isdir(dname):
	shutil.rmtree(dname)
shutil.move(fname+'/'+sname, dname)

print('Cleaning up...')
shutil.rmtree(fname)
os.remove(fname+'.zip')

url='http://www.reportlab.com/ftp/pfbfer-20070710.zip'
fname='Scripts/xhtml2pdf/fonts/pfbfer-20070710'
sname='pfbfer-20070710'
dname='Scripts/xhtml2pdf/fonts'
if os.path.isdir(dname):
	shutil.rmtree(dname)
os.mkdir(dname)
print('Downloading '+sname+'...')
urllib.urlretrieve(url, fname+'.zip')

print('Extracting...')
dr=os.getcwd()
os.chdir(dname)
with ZipFile(sname+'.zip', 'r') as z:
	z.extractall()
os.chdir(dr)

print('Cleaning up...')
os.remove(fname+'.zip')


editor.reload_files()
print('Done')

