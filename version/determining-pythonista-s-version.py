# coding: utf-8

# https://forum.omz-software.com/topic/2444/determining-pythonista-s-version

def PythonistaVersion():
	try:
		__import__('imp').find_module('dialogs')
		return 1.6
	except ImportError:
		return 1.5
		
print 'Pythonista Version is {}'.format(PythonistaVersion())


#==============================

# coding: utf-8
import timeit


def PythonistaVersion():
	try:
		__import__('imp').find_module('dialogs')
		return 1.6
	except ImportError:
		return 1.5
		
def PythonistaVersion2():
	try:
		import dialogs
		return 1.6
	except ImportError:
		return 1.5
		
		
		
print timeit.Timer('PythonistaVersion',setup="from __main__ import PythonistaVersion").timeit()

print timeit.Timer('PythonistaVersion2',setup="from __main__ import PythonistaVersion2").timeit()


#==============================

 def checkversion():
		import os, sys, plistlib
		plist=plistlib.readPlist(os.path.abspath(os.path.join(sys.executable,'../Info.plist')))
		return plist['CFBundleShortVersionString']'
		
#==============================

# coding: utf-8

# from @ccc omz forums

# Output: Pythonista version 1.6 (160037) on iOS 9.2 on an iPad3,4.
# Pythonista version 2.0.1 (201000) on iOS 9.2.1 on a 64-bit iPad5,4 with a screen size of (1024 x 768) * 2
# built on https://forum.omz-software.com/topic/2444/determining-pythonista-s-version/3

import os, platform, plistlib, scene, sys

def pythonista_info():  # 2.0.1 (201000)
	plist = plistlib.readPlist(os.path.abspath(os.path.join(sys.executable, '..', 'Info.plist')))
	
	ios_ver, _, machine_model = platform.mac_ver()
	
	return dict(
	pythonista_ver_str = plist['CFBundleShortVersionString'],
	pythonista_ver_num = plist['CFBundleVersion'],
	ios_ver_str = ios_ver,
	screen_resoultion = scene.get_screen_size(),
	screen_scale = scene.get_screen_scale(),
	machine_architecture = platform.architecture()[0],
	machine_model = machine_model,
	
	)
	
if __name__ == '__main__':
	print pythonista_info()

