# https://forum.omz-software.com/topic/3896/objc_tools-library/4

from objc_util import ObjCClass, ObjCBlock, c_void_p, ns, ObjCInstance

def getData(_cmd, pedometerData, error):
	ped = ObjCInstance(pedometerData)
	
	if not error == None:
		err = ObjCInstance(error)
		print('error===='+str(err))
	else:
		print('Steps===='+str(ped.numberOfSteps()))
		print('Distance===='+str(ped.distance()))
		
ped_block = ObjCBlock(getData, restype=None, argtypes=[c_void_p, c_void_p, c_void_p])
CMPedometer = ObjCClass('CMPedometer')
NSDate = ObjCClass('NSDate')

ped = CMPedometer.alloc().init()

if CMPedometer.isStepCountingAvailable():
	fromDate = NSDate.dateWithTimeIntervalSinceNow_(-60*60*24*2)
	toDate = NSDate.dateWithTimeIntervalSinceNow_(-60*60*24*1)
	ped.queryPedometerDataFromDate_toDate_withHandler_(ns(fromDate),ns(toDate),ped_block)
else:
	print('Unavailable')

