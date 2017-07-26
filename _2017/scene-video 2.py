# https://forum.omz-software.com/topic/4015/screen-recording-in-scene/3

# The draw_snapshot method is fine for static screenshots, but not nearly fast enough to record video.

# You can use objc_util to bridge the native ReplayKit framework. Here's a demo of that. It includes a very simple scene with some rotating space ships, just to have something to record... In this example, the recording is started in the scene's setup method, and stopped in its stop method (which is called automatically when the scene is about to be closed).

from objc_util import *
from scene import *
import random

load_framework('ReplayKit')
RPScreenRecorder = ObjCClass('RPScreenRecorder')

def previewControllerDidFinish_(_self, _cmd, _vc):
	ObjCInstance(_vc).dismissViewControllerAnimated_completion_(True, None)
	
PreviewDelegate = create_objc_class('PreviewDelegate', methods=[previewControllerDidFinish_])

def stop_callback(_cmd, _vc):
	vc = ObjCInstance(_vc)
	delegate = PreviewDelegate.new().autorelease()
	vc.setPreviewControllerDelegate_(delegate)
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
	
	
class MyScene (Scene):
	def setup(self):
		start_recording()
		for i in range(25):
			s = SpriteNode('spc:PlayerShip2Orange', position=(random.uniform(0, self.size.w), random.uniform(0, self.size.h)), parent=self)
			s.run_action(Action.repeat(Action.rotate_by(1, random.uniform(0.2, 0.8)), 0))
			
	def stop(self):
		stop_recording()
		
run(MyScene())

