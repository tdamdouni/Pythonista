# https://gist.github.com/lukaskollmer/44601c4bfef14fea7d0cf4a91a1542fd

import os
import sys
import plistlib

def get_bundle_identifier():
	plist = plistlib.readPlist(os.path.abspath(os.path.join(sys.executable, '..', 'Info.plist')))
	return '{CFBundleIdentifier}'.format(**plist)

def is_pythonista_3():
	return get_bundle_identifier() == 'com.omz-software.Pythonista3'

def is_pythonista_2():
	return get_bundle_identifier() == 'com.omz-software.Pythonista'

if __name__ == '__main__':
	print(is_pythonista_3())
	print(is_pythonista_2())
