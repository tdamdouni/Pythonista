# coding: utf-8

# https://github.com/jsbain/objc_hacks/blob/master/live_camera_view.py

# https://forum.omz-software.com/topic/2062/video-preview-inside-ui-view-beta

from objc_util import *
import ui

class LiveCameraView(ui.View):
	def __init__(self,device=0, *args, **kwargs):
		ui.View.__init__(self,*args,**kwargs)
		self._session=ObjCClass('AVCaptureSession').alloc().init()
		self._session.setSessionPreset_('AVCaptureSessionPresetHigh');
		inputDevices=ObjCClass('AVCaptureDevice').devices()
		self._inputDevice=inputDevices[device]
		
		deviceInput=ObjCClass('AVCaptureDeviceInput').deviceInputWithDevice_error_(self._inputDevice, None);
		if self._session.canAddInput_(deviceInput):
			self._session.addInput_(deviceInput)
		self._previewLayer=ObjCClass('AVCaptureVideoPreviewLayer').alloc().initWithSession_(self._session)
		self._previewLayer.setVideoGravity_(
		'AVLayerVideoGravityResizeAspectFill')
		rootLayer=ObjCInstance(self).layer()
		rootLayer.setMasksToBounds_(True)
		self._previewLayer.setFrame_(
		CGRect(CGPoint(-70, 0), CGSize(self.height,self.height)))
		rootLayer.insertSublayer_atIndex_(self._previewLayer,0)
		self._session.startRunning()
	def will_close(self):
		self._session.stopRunning()
	def layout(self):
		if not self._session.isRunning():
			self._session.startRunning()
			
rootview=LiveCameraView(frame=(0,0,576,576))
rootview.present('sheet')

