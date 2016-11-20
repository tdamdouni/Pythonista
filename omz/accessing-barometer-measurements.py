# coding: utf-8

# @omz

# https://forum.omz-software.com/topic/3078/accessing-barometer-measurements/5

from objc_util import ObjCInstance, ObjCClass, ObjCBlock, c_void_p

def handler(_cmd, _data, _error):
	print(ObjCInstance(_data))
	
handler_block = ObjCBlock(handler, restype=None, argtypes=[c_void_p, c_void_p, c_void_p])

def main():
	CMAltimeter = ObjCClass('CMAltimeter')
	NSOperationQueue = ObjCClass('NSOperationQueue')
	if not CMAltimeter.isRelativeAltitudeAvailable():
		print('This device has no barometer.')
		return
	altimeter = CMAltimeter.new()
	main_q = NSOperationQueue.mainQueue()
	altimeter.startRelativeAltitudeUpdatesToQueue_withHandler_(main_q, handler_block)
	print('Started altitude updates.')
	try:
		while True:
			pass
	finally:
		altimeter.stopRelativeAltitudeUpdates()
		print('Updates stopped.')
		
if __name__ == '__main__':
	main()

