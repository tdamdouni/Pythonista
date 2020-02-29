# coding: utf-8

# https://gist.github.com/mcsquaredjr/ce94c6ce121adb7540ff

# https://forum.omz-software.com/topic/141/set-reminders-in-evernote-with-pythonista-and-google-calendar

from __future__ import print_function
import tarfile
import shutil
import urllib
import requests
import os
import json


############################################################
#                 INSTALL EVERGREENCAL.PY                  #
############################################################
try:
	os.mkdir('evergreencal')
	json_url = 'https://api.github.com/gists/0e92cc9531d8ec28c0f8'
	gist_json = requests.get(json_url).text
	gist_info = json.loads(gist_json)
	files = gist_info['files']
	file_info = files.values()[0]
	filename = file_info['filename']
	content = file_info['content']
	
	print('Installing evergreencal.py...')
	f = open('evergreencal.py', 'w')
	f.write(content)
	f.close()
	shutil.move('evergreencal.py', 'evergreencal')
	print('evergreencal.py installed.')
except Exception as e:
	print(e)
	
	
############################################################
#                   INSTALL EVERNOTE SDK                   #
############################################################
try:
	os.mkdir('evernote-sdk')
	print('Downloading evernote...')
	filename, headers = urllib.urlretrieve('https://pypi.python.org/packages/source/e/evernote/evernote-1.23.2.tar.gz')
	print('Installing evernote...')
	t = tarfile.open(filename, 'r')
	t.extractall()
	t.close()
	shutil.move('evernote-1.23.2/lib/evernote', 'evernote-sdk/evernote')
	shutil.move('evernote-1.23.2/lib/thrift', 'evernote-sdk/thrift')
	shutil.rmtree('evernote-1.23.2')
	print('evernote-1.23.2 installed')
	
	print('Downloading httplib2...')
	filename, headers = urllib.urlretrieve('https://pypi.python.org/packages/source/h/httplib2/httplib2-0.7.7.tar.gz')
	print('Installing httplib2...')
	t = tarfile.open(filename, 'r')
	t.extractall()
	t.close()
	shutil.move('httplib2-0.7.7/python2/httplib2', 'evernote-sdk/httplib2')
	shutil.rmtree('httplib2-0.7.7')
	
	print('Downloading oauth2...')
	filename, headers = urllib.urlretrieve('https://pypi.python.org/packages/source/o/oauth2/oauth2-1.5.211.tar.gz')
	print('Installing oauth2...')
	t = tarfile.open(filename, 'r')
	t.extractall()
	t.close()
	shutil.move('oauth2-1.5.211/oauth2', 'evernote-sdk/oauth2')
	shutil.rmtree('oauth2-1.5.211')
	print('oauth2-1.5.211 installed')
	
except:
	pass
	
############################################################
#                    INSTALL GOOGLE API                    #
############################################################
try:
	os.mkdir('google-api')
	
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
	print('google-api-python-client-1.0 installed.')
	
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
	print('python-gflags-2.0 instaled.')
	
	print('Downloading httplib2...')
	filename, headers = urllib.urlretrieve('https://pypi.python.org/packages/source/h/httplib2/httplib2-0.7.7.tar.gz')
	print('Installing httplib2...')
	t = tarfile.open(filename, 'r')
	t.extractall()
	t.close()
	shutil.move('httplib2-0.7.7/python2/httplib2', 'google-api/httplib2')
	shutil.rmtree('httplib2-0.7.7')
	print('httplib2 installed.')
	
except:
	pass
	
############################################################
#                  INSTALL PARSEDATETIME                   #
############################################################
try:
	os.mkdir('parsedatetime')
	
	print('Downloading parsedatetime...')
	filename, headers = urllib.urlretrieve('https://github.com/bear/parsedatetime/archive/master.tar.gz')
	print('Installing parsedatetime...')
	t = tarfile.open(filename, 'r')
	t.extractall()
	t.close()
	
	shutil.move('parsedatetime-master/parsedatetime/__init__.py', 'parsedatetime')
	shutil.move('parsedatetime-master/parsedatetime/parsedatetime.py', 'parsedatetime')
	shutil.move('parsedatetime-master/parsedatetime/pdt_locales.py', 'parsedatetime')
	shutil.rmtree('parsedatetime-master')
	print('parsedatetime installed.')
except:
	pass
	
	
import editor
editor.reload_files()

print('All done.')

