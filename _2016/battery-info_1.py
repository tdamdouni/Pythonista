# https://pythonista-app.slack.com/archives/codinghelp/p1486753364001396

from objc_util import ObjCInstance, c
from ctypes import c_char_p, c_long, c_int, c_void_p, c_int32, c_int64, byref
from time import time
from objc_tools.objc_json import objc_to_dict
__all__ = ['Battery']

c.IOServiceMatching.argtypes=[c_char_p]
c.IOServiceMatching.restype = c_long
kIOMasterPortDefault=c_int.in_dll(c,'kIOMasterPortDefault')
srv=ObjCInstance(c.IOServiceMatching(b"IOPMPowerSource"))
c.IOServiceGetMatchingService.argtypes=[c_int, c_void_p]
c.IOServiceGetMatchingService.restype = c_void_p
powerSource = c.IOServiceGetMatchingService(kIOMasterPortDefault, srv);
#c.IOServiceGetMatchingService
c.IORegistryEntryCreateCFProperties.argtypes=[c_int64 ,c_void_p, c_void_p, c_int32 ]


class Battery (object):
	'''A Battery Object:
	The reason for this is to make releasing said object a lot easier'''
	
	def __init__(self):
		self._objc_ptr=c_void_p(0)
		c.IORegistryEntryCreateCFProperties(powerSource, byref(self._objc_ptr), None, 0);\
		self.timestamp = time()
		self.valid = True
		
	def objc(self):
		if self._objc_ptr:
			return ObjCInstance(self)
		else:
			raise ValueError('Operation on released object')
			
	def release(self):
		ObjCInstance(self).release()
		self.valid = False
		self._objc_ptr = None
		
	def __exit__(self, exc_type, exc_value, traceback):
		self.release()
		
	def __enter__(self):
		self.__init__()
		return self
		
	def get_dict(self):
		return objc_to_dict(self.objc())

