# https://forum.omz-software.com/topic/1554/accessing-the-led-flashlight/11

from objc_util import ObjCClass

def toggle_flashlight():
	AVCaptureDevice = ObjCClass('AVCaptureDevice')
	device = AVCaptureDevice.defaultDeviceWithMediaType_('vide')
	if not device.hasTorch():
		raise RuntimeError('Device has no flashlight')
	mode = device.torchMode()
	device.lockForConfiguration_(None)
	device.setTorchMode_((mode + 1) % 2)
	device.unlockForConfiguration()
	
if __name__ == '__main__':
	toggle_flashlight()

