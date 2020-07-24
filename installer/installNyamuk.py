#!/usr/bin/env python
# installNyamuk -- https://github.com/iwanbk/nyamuk
# download from github the nyamuk Python library and install it for Pythonista on iOS

#import nyamuk, sys # uncomment if you want to test if nyamuk is already installed
#print('got it...')
#sys.exit()

from __future__ import print_function
import os, shutil, urllib, zipfile

moduleName = 'nyamuk'
zipFileName = moduleName + '.zip'
mainDir = moduleName + '-main'
url = 'http://nodeload.github.com/iwanbk/nyamuk/zip/master'
 
print('Downloading ' + zipFileName + '...')
urllib.urlretrieve(url, zipFileName)
 
print('Extracting ' + zipFileName + '...')
with zipfile.ZipFile(zipFileName) as myZip:
    myZip.extractall()

print('Moving files to ' + moduleName + '...')
if os.path.isdir(moduleName):
	shutil.rmtree(moduleName)
shutil.move(mainDir + '/' + moduleName, './' + moduleName)
shutil.move(mainDir + '/test/pass-sub.py', './' + moduleName + 'Pass-sub.py')
shutil.move(mainDir + '/test/pubnya.py', './' + moduleName + 'Pubnya.py')
shutil.move(mainDir + '/test/subnya.py', './' + moduleName + 'Subnya.py')

print('Cleaning up...')
shutil.rmtree(mainDir)
os.remove(zipFileName)
print('Done.')

# use dir() to view functions, variables, modules, etc.
import nyamuk, nyamuk.base_nyamuk, nyamuk.nyamuk_const, nyamuk.mqtt_pkt
import nyamuk.nyamuk_msg, nyamuk.nyamuk_net, nyamuk.event
print('\ndir(nyamuk):\n' + str(dir(nyamuk)))
import nyamuk.base_nyamuk
print('\ndir(nyamuk.base_nyamuk):\n' + str(dir(nyamuk.base_nyamuk)))
import nyamuk.nyamuk_const as NC
print('\ndir(nyamuk.nyamuk_const):\n' + str(dir(nyamuk.nyamuk_const)))
import nyamuk.mqtt_pkt as MqttPkt
print('\ndir(nyamuk.mqtt_pkt):\n' + str(dir(nyamuk.mqtt_pkt)))
import nyamuk.nyamuk_msg as NyamukMsgAll
print('\ndir(nyamuk.nyamuk_msg):\n' + str(dir(nyamuk.nyamuk_msg)))
import nyamuk.nyamuk_net
print('\ndir(nyamuk.nyamuk_net):\n' + str(dir(nyamuk.nyamuk_net)))
import nyamuk.event
print('\ndir(nyamuk.event):\n' + str(dir(nyamuk.event)))
