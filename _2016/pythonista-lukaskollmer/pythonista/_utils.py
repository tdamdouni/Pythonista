# https://github.com/lukaskollmer/pythonista

"""
Utilities for the pythonista package
"""

__author__ = "Lukas Kollmer<lukas.kollmer@gmail.com>"
__copyright__ = "Copyright (c) 2016 Lukas Kollmer<lukas.kollmer@gmail.com>"


try:
	import objc_util
	_HAS_OBJC_UTIL = True
	_application = objc_util.UIApplication.sharedApplication()
except:
	_HAS_OBJC_UTIL = False

def guard_objc_util():
	if not _HAS_OBJC_UTIL: raise ImportError("objc_util not available")

def add_method(method, cls):
	guard_objc_util()
	import ctypes
	import objc_util
	import uuid
	
	encoding = "v@:"
	
	# this code is borrowed from `objc_util._add_method`
	parsed_types = objc_util.parse_types(encoding)
	restype = parsed_types[0]
	argtypes = parsed_types[1]
	IMPTYPE = ctypes.CFUNCTYPE(restype, *argtypes)
	imp = IMPTYPE(method)
	objc_util.retain_global(imp)
	
	selector = objc_util.sel(str(uuid.uuid1()).replace("-", ""))
	objc_util.class_addMethod(objc_util.object_getClass(cls.ptr), selector, imp, encoding.encode("ascii"))
	return selector
