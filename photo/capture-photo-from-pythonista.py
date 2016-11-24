# @tdamdouni gists
# https://gist.github.com/44887d69c3ab603d4a4c1652cb08435b

# https://forum.omz-software.com/topic/3665/capturing-photos-without-the-ios-screen

from objc_util import *
import time
import threading
C = ObjCClass

def take_photo_now(filename='photo.jpg'):
	session = C('AVCaptureSession').new().autorelease()
	session.sessionPreset = 'AVCaptureSessionPresetPhoto'
	device = C('AVCaptureDevice').defaultDeviceWithMediaType_('vide')
	device_input = C('AVCaptureDeviceInput').deviceInputWithDevice_error_(device, None)
	session.addInput_(device_input)
	image_output = C('AVCaptureStillImageOutput').new().autorelease()
	session.addOutput_(image_output)
	session.startRunning()
	# NOTE: You may need to adjust this to wait for the camera to be ready (use a higher number if you see black photos):
	time.sleep(0.1)
	def handler_func(_block, _buffer, _err):
		buffer = ObjCInstance(_buffer)
		img_data = C('AVCaptureStillImageOutput').jpegStillImageNSDataRepresentation_(buffer)
		img_data.writeToFile_atomically_(filename, True)
		e.set()
	video_connection = None
	for connection in image_output.connections():
		for port in connection.inputPorts():
			if str(port.mediaType()) == 'vide':
				video_connection = connection
				break
		if video_connection:
			break
	e = threading.Event()
	handler = ObjCBlock(handler_func, restype=None, argtypes=[c_void_p, c_void_p, c_void_p])
	retain_global(handler)
	image_output.captureStillImageAsynchronouslyFromConnection_completionHandler_(video_connection, handler)
	e.wait()
	
	
take_photo_now('photo.jpg')
import console
console.quicklook('photo.jpg')

