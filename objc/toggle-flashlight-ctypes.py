# coding: utf-8

# @omz

# https://forum.omz-software.com/topic/1554/accessing-the-led-flashlight/3

from ctypes import c_void_p, c_char_p, c_int, c_bool, cdll

objc = cdll.LoadLibrary(None)
objc.sel_getName.restype = c_char_p
objc.sel_getName.argtypes = [c_void_p]
objc.sel_registerName.restype = c_void_p
objc.sel_registerName.argtypes = [c_char_p]
objc.objc_getClass.argtypes = [c_char_p]
objc.objc_getClass.restype = c_void_p

# Some helper methods:
def msg(obj, restype, sel, argtypes=None, *args):
	if argtypes is None:
		argtypes = []
	objc.objc_msgSend.argtypes =  [c_void_p, c_void_p] + argtypes
	objc.objc_msgSend.restype = restype
	res = objc.objc_msgSend(obj, objc.sel_registerName(sel), *args)
	return res
	
def cls(cls_name):
	return objc.objc_getClass(cls_name)
	
def nsstr(s):
	return msg(cls('NSString'), c_void_p, 'stringWithUTF8String:', [c_char_p], s)
	
def toggle_flashlight():
	AVCaptureDevice = cls('AVCaptureDevice')
	device = msg(AVCaptureDevice, c_void_p, 'defaultDeviceWithMediaType:', [c_void_p], nsstr('vide'))
	has_torch = msg(device, c_bool, 'hasTorch')
	if not has_torch:
		raise RuntimeError('Device has no flashlight')
	current_mode = msg(device, c_int, 'torchMode')
	mode = 1 if current_mode == 0 else 0
	msg(device, None, 'lockForConfiguration:', [c_void_p], None)
	msg(device, None, 'setTorchMode:', [c_int], mode)
	msg(device, None, 'unlockForConfiguration')
	
if __name__ == '__main__':
	toggle_flashlight()

