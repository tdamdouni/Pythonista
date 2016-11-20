# coding: utf-8

# https://forum.omz-software.com/topic/2060/presenting-viewcontroller/3

from objc_util import *
def get_view_controller(uiview):
	if isinstance(uiview,ui.View):
		viewobj=ObjCInstance(uiview)
	elif isa(uiview,'ObjCInstance') and uiview.isKindOfClass_(ObjCClass('UIView')):
		viewobj=uiview
	viewResponder=viewobj.nextResponder()
	try:
		while not viewResponder.isKindOfClass_(ObjCClass('UIViewController')):
			viewResponder=viewResponder.nextResponder()
		except AttributeError:
			return None #if view is not being presented for example
	return viewResponder
	
# --------------------

root_view_controller= get_view_controller(root)
someothercontroller.view().setFrame_(ObjCInstance(root).bounds())
ObjCInstance(root).addSubview_(someothercontroller.view())
root_view_controller.addChildViewVontroller(someothercontroller)
someothercontroller.didMoveToParentViewController_(root_view_controller)

# --------------------

from objc_util import *
from time import sleep
#import objutil

ObjCClass('NSBundle').bundleWithPath_('/System/Library/Frameworks/ReplayKit.framework').load()

recorder=ObjCClass('RPScreenRecorder')
preview=ObjCClass('RPPreviewViewController')
sharedrecorder=recorder.sharedRecorder()
sharedrecorder.startRecordingWithMicrophoneEnabled_handler_(False,None)#(false,none)

print 'Recording:' + str(sharedrecorder.isRecording())
print 'Microphone Enabled:' + str(sharedrecorder.isMicrophoneEnabled())
sleep(3)
#Some cool things...

#Stopping the recording and saving
print 'Stopping...'
sharedrecorder.stopRecordingWithHandler_(preview)
app = ObjCClass('UIApplication').sharedApplication()
rootvc=app.keyWindow().rootViewController()
rootvc.presentViewController_animated_completion_(preview, True, None)

# --------------------

from objc_util import *
import time

NSBundle = ObjCClass('NSBundle')
replaykit = NSBundle.bundleWithPath_('/System/Library/Frameworks/ReplayKit.framework')
replaykit.load()

RPScreenRecorder = ObjCClass('RPScreenRecorder')

def stop_callback(_cmd, _vc):
	vc = ObjCInstance(_vc)
	rootvc = UIApplication.sharedApplication().keyWindow().rootViewController()
	vc.popoverPresentationController().setSourceView_(rootvc.view())
	rootvc.presentViewController_animated_completion_(vc, True, None)
	
stop_handler = ObjCBlock(stop_callback, restype=None, argtypes=[c_void_p, c_void_p])

recorder = RPScreenRecorder.sharedRecorder()

@on_main_thread
def start_recording():
	recorder.startRecordingWithMicrophoneEnabled_handler_(False, None)
	
@on_main_thread
def stop_recording():
	recorder.stopRecordingWithHandler_(stop_handler)
	
start_recording()
time.sleep(5)
stop_recording()

# --------------------

