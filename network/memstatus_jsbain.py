# https://gist.github.com/jsbain/3f358f4ea224a18c35a3a4aac0a8bd1e

from objc_util import c
import ctypes
def _get_taskinfo():
	integer_t = ctypes.c_int
	natural_t = ctypes.c_uint
	vm_size_t = ctypes.c_ulong
	
	class time_value_t(ctypes.Structure):
		_fields_ = [("seconds", integer_t),
		("microseconds", integer_t)]
		
		def __repr__(self):
			return "%s.%s" % (self.seconds, self.microseconds)
			
	policy_t = ctypes.c_int
	
	class task_basic_info(ctypes.Structure):
		_pack_ = 4
		_fields_ = [("suspend_count", integer_t),
		("virtual_size", vm_size_t),
		("resident_size", vm_size_t),
		("user_time", time_value_t),
		("system_time", time_value_t),
		("policy", policy_t)]
		
		def __repr__(self):
			return repr(dict((key, getattr(self, key))
			for key in dir(self)
			if not key.startswith("_")))
			
	kern_return_t = ctypes.c_int
	mach_port_t = natural_t
	task_name_t = ctypes.c_uint
	task_flavor_t = ctypes.c_uint
	task_info_t = ctypes.POINTER(ctypes.c_int)
	mach_msg_type_number_t = natural_t
	TASK_BASIC_INFO_COUNT = ctypes.sizeof(
	task_basic_info) // ctypes.sizeof(natural_t)
	TASK_BASIC_INFO = 5
	KERN_SUCCESS = 0
	
	libkern = c
	task_info = libkern.task_info
	task_info.restype = kern_return_t
	task_info.argtypes = [task_name_t,
	task_flavor_t,
	ctypes.POINTER(task_basic_info),
	ctypes.POINTER(mach_msg_type_number_t)]
	
	mach_task_self = libkern.mach_task_self
	mach_task_self.restype = mach_port_t
	mach_task_self.argtypes = []
	
	ti = task_basic_info()
	
	count = mach_msg_type_number_t(TASK_BASIC_INFO_COUNT)
	kr = task_info(mach_task_self(), TASK_BASIC_INFO,
	ctypes.byref(ti),
	ctypes.byref(count))
	if kr != KERN_SUCCESS:
		return None
	return ti

