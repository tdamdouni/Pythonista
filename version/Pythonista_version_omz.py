# coding: utf-8

# https://forum.omz-software.com/topic/2794/old-bugs/6

from __future__ import print_function
def pythonista_version():
	try:
		# Try reading Info.plist using plistlib; could fail if Info.plist is binary
		plist = plistlib.readPlist(os.path.abspath(os.path.join(sys.executable, '..', 'Info.plist')))
		return '{CFBundleShortVersionString} ({CFBundleVersion})'.format(**plist)
	except:
		try:
			# Use objc_util to access Info.plist via native APIs; will fail for versions < 2.0 (objc_util/ctypes weren't available)
			from objc_util import NSBundle
			return str(NSBundle.mainBundle().infoDictionary()['CFBundleShortVersionString'])
		except ImportError:
			# For older versions (1.x), determine the version by checking for capabilities (modules that were added)
			version = None
			try:
				import ui
				version = '1.5'
			except ImportError:
				pass
			if not version:
				try:
					import contacts
					version = '1.4'
				except ImportError:
					pass
			if not version:
				try:
					import photos
					version = '1.3'
				except ImportError:
					pass
			if not version:
				try:
					import PIL
					version = '1.2'
				except ImportError:
					pass
			if not version:
				try:
					import editor
					version = '1.1'
				except ImportError:
					pass
			if not version:
				version = '1.0'
			return version
print(version)

