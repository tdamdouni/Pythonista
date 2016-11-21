import os

import objc
import objc_util

objc.classes.NSBundle.bundleWithPath_("/System/Library/Frameworks/AVFoundation.framework").load()

objc.ffi.cdef("""
extern id AVCaptureSessionPresetPhoto;

extern id AVMediaTypeVideo;
""")

def captureOutput_didFinishProcessingRawPhotoSampleBuffer_previewPhotoSampleBuffer_resolvedSettings_bracketSettings_error_(self, _cmd, cout, buf, prevbuf, resset, brackset, err):
	global stuff, dat
	
	self = objc.ID(self or 0)
	_cmd = objc.Selector(_cmd or 0)
	cout = objc.ID(cout or 0)
	buf = objc.ID(buf or 0)
	prevbuf = objc.ID(prevbuf or 0)
	resset = objc.ID(resset or 0)
	brackset = objc.ID(brackset or 0)
	err = objc.ID(err or 0)
	
	print("Updating stuff")
	stuff = (
		self,
		_cmd,
		cout,
		buf,
		prevbuf,
		resset,
		brackset,
		err,
	)
	print("Updating dat")
	dat = objc.classes.AVCapturePhotoOutput.DNGPhotoDataRepresentationForRawSampleBuffer_previewPhotoSampleBuffer_(buf or objc.ffi.NULL, prevbuf or objc.ffi.NULL, restype="id", argtypes=["id", "id"])
	print("Updated dat")
	dat.writeToFile_atomically_(os.path.expanduser("~/Documents/foo.dng"), False)
	print("Wrote foo.dng")

DGCaptureDelegate = objc.Class(objc_util.create_objc_class(
	name="DGCaptureDelegate",
	superclass=objc_util.NSObject,
	protocols=["AVCapturePhotoDelegate"],
	methods=[
		captureOutput_didFinishProcessingRawPhotoSampleBuffer_previewPhotoSampleBuffer_resolvedSettings_bracketSettings_error_,
	],
))

if __name__ == "__main__":
	sess = objc.classes.AVCaptureSession.new()
	
	sess.setSessionPreset_(objc.libc.AVCaptureSessionPresetPhoto)
	
	cam = objc.classes.AVCaptureDevice.defaultDeviceWithMediaType_(objc.libc.AVMediaTypeVideo)
	
	capin = objc.classes.AVCaptureDeviceInput.deviceInputWithDevice_error_(cam, objc.ffi.NULL)
	capout = objc.classes.AVCapturePhotoOutput.new()
	
	sess.addInput_(capin)
	sess.addOutput_(capout)
	
	ps = objc.classes.AVCapturePhotoSettings.photoSettingsWithRawPixelFormatType_(capout.availableRawPhotoPixelFormatTypes().objectAtIndex_(0).intValue())
	
	try:
		sess.startRunning()
		capout.capturePhotoWithSettings_delegate_(ps, DGCaptureDelegate.new())
	finally:
		sess.stopRunning()


