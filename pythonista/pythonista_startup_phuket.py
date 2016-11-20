# coding: utf-8

# https://forum.omz-software.com/topic/3607/change-font-in-console

import sys, os, console

print('my startup script\n')
from objc_util import *
UIScreen = ObjCClass('UIScreen')
from plistlib import readPlist


screen = UIScreen.mainScreen()
screen.setBrightness_(0.25)

UIView.beginAnimations_(None)
UIView.setAnimationDuration_(0)
print('switching off animations\n')

print('screen brightness:'.upper(), '{:f}'.format(screen.brightness()))

fnt = ('Menlo', 22)
console.set_font(*fnt)
print('Font set to {}-{}'.format(*fnt))

def pyst_version_str():
	plist = readPlist(os.path.abspath(os.path.join(sys.executable, '..', 'Info.plist')))
	return plist['CFBundleShortVersionString']
	
print(('Pythonista Version:{}'.format(pyst_version_str())))

