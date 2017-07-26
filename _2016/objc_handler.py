# https://github.com/scj643/objc_tools/blob/master/objc_tools/c/objc_handler.py

from objc_util import ObjCInstance, c_void_p

def chandle(result, func, args):
	'''chandle
	Handles c_void_p to objc type
	use as a errcheck for a ctypes function
	>>> cfunc.restype = c_void_p
	>>> cfunc.errcheck = chandle
	'''
	if isinstance(result, (c_void_p, int)) and result:
		return ObjCInstance(result)
		
		
if __name__ == '__main__':
	from objc_util import *
	from objc_util import c
	MRMediaRemoteCopyPickableRoutes = c.MRMediaRemoteCopyPickableRoutes
	MRMediaRemoteCopyPickableRoutes.restype = c_void_p
	MRMediaRemoteCopyPickableRoutes.errcheck = chandle
	t=MRMediaRemoteCopyPickableRoutes()

