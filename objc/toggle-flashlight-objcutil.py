# https://forum.omz-software.com/topic/1554/accessing-the-led-flashlight/20

from objc_util import ObjCClass
import time

def toggle_flashlight():
	AVCaptureDevice = ObjCClass('AVCaptureDevice')
	device = AVCaptureDevice.defaultDeviceWithMediaType_('vide')
	if not device.hasTorch():
		raise RuntimeError('Device has no flashlight')
	mode = device.torchMode()
	device.lockForConfiguration_(None)
	if device.torchMode()>0:
		device.setTorchMode_((mode + 1) % 2)
	else:
		a =[1.0,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1]
		
		for each in a:
		
			device.setTorchModeOnWithLevel_error_(each, None)
			print('level '+str(each))
			time.sleep(.6)
			
		#device.setTorchModeOnWithLevel_error_(0.88, None)
		
		
	device.unlockForConfiguration()
	#device.setTorchModeOnWithLevel_error_(0.2, None)
	
	
	
if __name__ == '__main__':
	toggle_flashlight()

