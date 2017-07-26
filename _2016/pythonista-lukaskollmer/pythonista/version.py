# https://github.com/lukaskollmer/pythonista

"""
Use this module to get the current version of the app
"""

__author__ = "Lukas Kollmer<lukas.kollmer@gmail.com>"
__copyright__ = "Copyright (c) 2016 Lukas Kollmer<lukas.kollmer@gmail.com>"

from pythonista._utils import _HAS_OBJC_UTIL

def version():
	'''
	Get the version of Pythonista
	'''
	
	if _HAS_OBJC_UTIL:
		import objc_util
		infoDictionary = objc_util.NSBundle.mainBundle().infoDictionary()
		version = str(infoDictionary['CFBundleShortVersionString'])
		build = str(infoDictionary['CFBundleVersion'])
		return (version, build)
	else:
		import plistlib
		plist = plistlib.readPlist(os.path.abspath(os.path.join(sys.executable, '..', 'Info.plist')))
		return ('{CFBundleShortVersionString}'.format(**plist), '{CFBundleVersion}'.format(**plist))

if __name__ == "__main__":
	print('version: {}'.format(version()))
