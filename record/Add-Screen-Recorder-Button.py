# coding: utf-8

# https://gist.github.com/Dutcho/d6dca2ac48ef96801417

from __future__ import print_function
from objc_util import *
from UIKit import *
from Foundation import *
from ReplayKit import *
from console import alert

def main():
	rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
	tabVC = rootVC.detailViewController()
	
	methods = [screenRecorderButtonPressed]
	ScreenRecorderItemController = create_objc_class('ScreenRecorderItemController', NSObject, methods = methods)
	
	screenRecorderItemController = ScreenRecorderItemController.new()
	
	try:
		ScreenRecorderBarButtonItem = ObjCClass('ScreenRecorderBarButtonItem')
	except ValueError:
		ScreenRecorderBarButtonItem = create_objc_class('ScreenRecorderBarButtonItem', UIBarButtonItem)
	
	screenRecorderItem = ScreenRecorderBarButtonItem.alloc().initWithImage_style_target_action_(ns(ui.Image.named('iob:ios7_videocam_outline_32')), 0, screenRecorderItemController, sel('screenRecorderButtonPressed'))
	screenRecorderItemController.screenRecorderItem = screenRecorderItem
	
	leftBarButtonItems = list(tabVC.persistentLeftBarButtonItems())
	leftBarButtonItems.append(screenRecorderItem)
	tabVC.persistentLeftBarButtonItems = ns(leftBarButtonItems)
	tabVC.reloadBarButtonItemsForSelectedTab()

def screenRecorderButtonPressed(_self, _cmd):
	from objc_util import ObjCInstance, CGRect
	from ReplayKit import RPScreenRecorder
	from console import alert
	from UIKit import UILabel, UISwitch, UIApplication, UIFont
	import ShowTouches
	rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
	tabVC = rootVC.detailViewController()
	screenRecorderItem = None
	for item in tabVC.persistentLeftBarButtonItems():
		if item._get_objc_classname().endswith('ScreenRecorderBarButtonItem'):
			screenRecorderItem = item
	recorder = RPScreenRecorder.sharedRecorder()
	if recorder.isRecording():
		def recordingStoppedHandler(_cmd, _previewViewController, _error):
			if _previewViewController:
				screenRecorderItem.image = ns(ui.Image.named('iob:ios7_videocam_outline_32'))
				ShowTouches.set_show_touches(False)
				previewViewController = ObjCInstance(_previewViewController)
				def previewControllerDidFinish_(_self, _cmd, _previewViewController):
					previewViewController = ObjCInstance(_previewViewController)
					rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
					on_main_thread(rootVC.dismissViewControllerAnimated_completion_)(True, None)
				PreviewControllerDelegate = create_objc_class('PreviewControllerDelegate', NSObject, protocols = ['RPPreviewViewControllerDelegate'], methods = [previewControllerDidFinish_])
				previewViewController.previewControllerDelegate = PreviewControllerDelegate.new()
				previewViewController.modalPresentationStyle = 0
				rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
				rootVC.presentViewController_animated_completion_(previewViewController, True, None)
			if _error:
				error = ObjCInstance(_error)
				print(error)
			
		recordingStoppedHandlerBlock = ObjCBlock(recordingStoppedHandler, None, [c_void_p, c_void_p, c_void_p])
		retain_global(recordingStoppedHandlerBlock)
		recorder.stopRecordingWithHandler_(recordingStoppedHandlerBlock)
	else:
		#micEnabled = not bool(alert('Record Screen', 'Start recording Pythonista?', 'Start Recording with Mic', 'Start Recording without Mic') - 1)
		screenRecorderSetingsAlert = UIAlertController.alertControllerWithTitle_message_preferredStyle_('Record Screen', '\n\n\n\n', 1)
		w = screenRecorderSetingsAlert.view().size().width
		micLabel = UILabel.alloc().initWithFrame_(CGRect((25, 50), ((175, 31))))
		micLabel.text = 'Record Microphone'
		micLabel.font = UIFont.systemFontOfSize_weight_(17, -1)
		global micSwitch
		micSwitch = UISwitch.alloc().initWithFrame_(CGRect((199, 50), (51, 31)))
		screenRecorderSetingsAlert.view().addSubview_(micLabel)
		screenRecorderSetingsAlert.view().addSubview_(micSwitch)
		touchesLabel = UILabel.alloc().initWithFrame_(CGRect((25, 95), ((175, 31))))
		touchesLabel.text = 'Show Touches'
		touchesLabel.font = UIFont.systemFontOfSize_weight_(17, -1)
		global touchesSwitch
		touchesSwitch = UISwitch.alloc().initWithFrame_(CGRect((199, 95), (51, 31)))
		screenRecorderSetingsAlert.view().addSubview_(touchesLabel)
		screenRecorderSetingsAlert.view().addSubview_(touchesSwitch)
		screenRecorderSetingsAlert.addAction_(UIAlertAction.actionWithTitle_style_handler_('Close', 1, None))
		def alertActionStartRecording(action):
			global micSwitch, touchSwitch
			micEnabled = micSwitch.on()
			showTouches = touchesSwitch.on()
			def recordingStartedHandler(_self, _cmd, _error):
				if _error:
					error = ObjCInstance(_error)
					print(error.localizedDescription())
				elif RPScreenRecorder.sharedRecorder().isRecording():
					screenRecorderItem.image = ns(ui.Image.named('iob:ios7_videocam_32'))
					ShowTouches.set_show_touches(showTouches)
			recordingStartedHandlerBlock = ObjCBlock(recordingStartedHandler, None, [c_void_p, c_void_p, c_void_p])
			retain_global(recordingStartedHandlerBlock)
			if recorder.isAvailable():
				recorder.startRecordingWithMicrophoneEnabled_handler_(micEnabled, recordingStartedHandlerBlock)
		
		alertActionStartRecordingBlock = ObjCBlock(alertActionStartRecording, None, [c_void_p])
		retain_global(alertActionStartRecordingBlock)
		screenRecorderSetingsAlert.addAction_(UIAlertAction.actionWithTitle_style_handler_('Start Recording', 0, alertActionStartRecordingBlock))
		UIApplication.sharedApplication().keyWindow().rootViewController().presentViewController_animated_completion_(screenRecorderSetingsAlert, True, None)

if __name__ == '__main__':
	main()
