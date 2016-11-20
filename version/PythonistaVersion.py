# coding: utf-8

# https://forum.omz-software.com/topic/2444/determining-pythonista-s-version

import os, sys, plistlib
def checkversion():
	plist=plistlib.readPlist(os.path.abspath(os.path.join(sys.executable,'../Info.plist')))
return plist['CFBundleShortVersionString']'
