# coding: utf-8

# https://forum.omz-software.com/topic/2743/new-xcode-template-on-github/13

from __future__ import print_function
from objc_util import NSBundle

info = NSBundle.mainBundle().infoDictionary()
version = str(info['CFBundleVersion'])
short_version = str(info['CFBundleShortVersionString'])
print(version)