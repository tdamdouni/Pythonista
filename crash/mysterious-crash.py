# coding: utf-8

# https://forum.omz-software.com/topic/3099/mysterious-crash

from ctypes import POINTER
from objc_util import ObjCClass, ObjCInstance, c, c_void_p


NSHomeDirectory = c.NSHomeDirectory
NSHomeDirectory.restype = c_void_p
NSHomeDirectory.argtype = []

NSFileManager = ObjCClass('NSFileManager')

LP_c_void_p = POINTER(c_void_p)

def get_system_attributes():
	file_manager = NSFileManager.defaultManager()
	error = LP_c_void_p()
	attributes = file_manager.attributesOfFileSystemForPath_error_(
	ObjCInstance(
	NSHomeDirectory()
	).cString(),
	error
	)
	return attributes
	
get_system_attributes()

#from ctypes import pointer
#from objc_util import ObjCClass, ObjCInstance, c, c_void_p
#path = ObjCInstance(NSHomeDirectory())
#file_manager = NSFileManager.defaultManager()
#error = c_void_p()
#a = file_manager.attributesOfFileSystemForPath_error_(path, pointer(error))
#print(ObjCInstance(error))
#print(a)

