#!python2
# coding: utf-8

# https://gist.github.com/omz/11891cb1c7ed459d34c7

# Barcode scanner demo for Pythonista
# Based on http://www.infragistics.com/community/blogs/torrey-betts/archive/2013/10/10/scanning-barcodes-with-ios-7-objective-c.aspx

from objc_util import *
from ctypes import c_void_p
import ui
import sound

found_codes = set()
main_view = None

AVCaptureSession = ObjCClass('AVCaptureSession')
AVCaptureDevice = ObjCClass('AVCaptureDevice')
AVCaptureDeviceInput = ObjCClass('AVCaptureDeviceInput')
AVCaptureMetadataOutput = ObjCClass('AVCaptureMetadataOutput')
AVCaptureVideoPreviewLayer = ObjCClass('AVCaptureVideoPreviewLayer')
dispatch_get_current_queue = c.dispatch_get_current_queue
dispatch_get_current_queue.restype = c_void_p

def captureOutput_didOutputMetadataObjects_fromConnection_(_self, _cmd, _output, _metadata_objects, _conn):
	objects = ObjCInstance(_metadata_objects)
	for obj in objects:
		s = str(obj.stringValue())
		if s not in found_codes:
			found_codes.add(s)
			sound.play_effect('digital:PowerUp7')
		main_view['label'].text = 'Last scan: ' + s

MetadataDelegate = create_objc_class('MetadataDelegate', methods=[captureOutput_didOutputMetadataObjects_fromConnection_], protocols=['AVCaptureMetadataOutputObjectsDelegate'])

@on_main_thread
def main():
	global main_view
	delegate = MetadataDelegate.new()
	main_view = ui.View(frame=(0, 0, 400, 400))
	main_view.name = 'Barcode Scanner'
	session = AVCaptureSession.alloc().init()
	device = AVCaptureDevice.defaultDeviceWithMediaType_('vide')
	_input = AVCaptureDeviceInput.deviceInputWithDevice_error_(device, None)
	if _input:
		session.addInput_(_input)
	else:
		print('Failed to create input')
		return
	output = AVCaptureMetadataOutput.alloc().init()
	queue = ObjCInstance(dispatch_get_current_queue())
	output.setMetadataObjectsDelegate_queue_(delegate, queue)
	session.addOutput_(output)
	output.setMetadataObjectTypes_(output.availableMetadataObjectTypes())
	prev_layer = AVCaptureVideoPreviewLayer.layerWithSession_(session)
	prev_layer.frame = ObjCInstance(main_view).bounds()
	prev_layer.setVideoGravity_('AVLayerVideoGravityResizeAspectFill')
	ObjCInstance(main_view).layer().addSublayer_(prev_layer)
	label = ui.Label(frame=(0, 0, 400, 30), flex='W', name='label')
	label.background_color = (0, 0, 0, 0.5)
	label.text_color = 'white'
	label.text = 'Nothing scanned yet'
	label.alignment = ui.ALIGN_CENTER
	main_view.add_subview(label)
	session.startRunning()
	main_view.present('sheet')
	main_view.wait_modal()
	session.stopRunning()
	delegate.release()
	session.release()
	output.release()
	if found_codes:
		print 'All scanned codes:\n' + '\n'.join(found_codes)

if __name__ == '__main__':
	main()
