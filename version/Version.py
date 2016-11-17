# coding: utf-8

import plistlib


def pyst_version_str():
	plist=plistlib.readPlist(os.path.abspath(os.path.join(
	sys.executable, '''../Info.plist''')))

	return plist['CFBundleShortVersionString']
