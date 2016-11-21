# coding: utf-8

# https://forum.omz-software.com/topic/2747/python-3-x-progress-update/251

from objc_util import ObjCClass
ObjCClass('NSUserDefaults').standardUserDefaults().setBool_forKey_(True, 'EditorShowLineNumbersOnPhone')
