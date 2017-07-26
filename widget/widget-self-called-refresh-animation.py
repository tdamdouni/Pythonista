#!python3

# https://forum.omz-software.com/topic/3830/widget-self-called-refresh-animation

from objc_util import *
import os, ui
import appex
import time

def record():
	AVAudioSession = ObjCClass('AVAudioSession')
	NSURL = ObjCClass('NSURL')
	AVAudioRecorder = ObjCClass('AVAudioRecorder')
	shared_session = AVAudioSession.sharedInstance()
	category_set = shared_session.setCategory_error_(ns('AVAudioSessionCategoryPlayAndRecord'), None)
	settings = {ns('AVFormatIDKey'): ns(1633772320), ns('AVSampleRateKey'):ns(0.5), ns('AVNumberOfChannelsKey'):ns(1)}
	output_path = os.path.abspath('Recording.m4a')
	out_url = NSURL.fileURLWithPath_(ns(output_path))
	recorder = AVAudioRecorder.alloc().initWithURL_settings_error_(out_url, settings, None)
	recorder.record()
	recorder.setMeteringEnabled_(True)
	return recorder
	
label = ui.Label()
label.text = 'Please wait...'
label.font = ('Menlo', 75)
label.alignment = ui.ALIGN_CENTER
label.text_color = 'blue'
appex.set_widget_view(label)
recorder = record()
while True:
	recorder.updateMeters()
	label.text = str(recorder.peakPowerForChannel_(0))[: 6] + ' dB'
	label.set_needs_display()
	time.sleep(.25)
# --------------------
def loop():
	# add an exit criteria
	if some_criteria:
		return
	ui.delay(loop, 0.25)
	# do stuff
ui.delay(loop,0)
# --------------------

