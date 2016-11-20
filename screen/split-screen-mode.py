# coding: utf-8

# https://forum.omz-software.com/topic/2747/python-3-x-progress-update/326

from objc_util import ObjCClass
ObjCClass('NSUserDefaults').standardUserDefaults().setBool_forKey_(False, 'DockedAccessoriesPanel')

