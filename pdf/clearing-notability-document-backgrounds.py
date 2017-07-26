# coding: utf-8

# https://forum.omz-software.com/topic/3915/clearing-notability-document-backgrounds

import console, shutil, appex, os.path, zipfile, os, glob, re, plistlib

# Install biplist (I could not get plistlib to read the plist file, even
# when I used fmt=plistlib.FMT_BINARY))
# Rather than using pip, I just put the contents of this url in ./lib/biplist.py
# https://raw.githubusercontent.com/wooster/biplist/master/biplist/__init__.py

from lib.biplist import *

tmpPath = './jtziptmp/'
extractedPath = './jtziptmp/extracted/'
tmpFileName = 'tmpfile.zip'
newFileName = tmpPath+os.path.basename(appex.get_file_path())+'_bgstripped.note'
shutil.rmtree(tmpPath)
os.mkdir(tmpPath)
os.mkdir(extractedPath)
shutil.copy(appex.get_file_path(),tmpPath+tmpFileName)
shutil.unpack_archive(tmpPath+tmpFileName,extractedPath)

pattern = "^.*pdf$"
mypath = extractedPath
for root, dirs, files in os.walk(mypath):
	for file in filter(lambda x: re.match(pattern, x), files):
		os.remove(os.path.join(root, file)) # remove the pdf bg
		
pattern = "^Session.plist$"
mypath = extractedPath
for root, dirs, files in os.walk(mypath):
	for file in filter(lambda x: re.match(pattern, x), files):
		plist = readPlist(os.path.join(root, file))
		plist['$objects'][1]['paperIndex'] = 12 # set white bg
		writePlist(plist,os.path.join(root, file))
		
shutil.make_archive(newFileName,'zip',extractedPath)
shutil.move(newFileName+'.zip',newFileName)
console.open_in(newFileName)
# --------------------

