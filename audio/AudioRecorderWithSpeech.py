# Pythonista 1.6 Beta / Audio Recorder by omz
# https://gist.github.com/omz/9882a00abf59c6009fa4
from ctypes import c_void_p, c_char_p, c_double, c_float, c_int, cdll, util, c_bool
import os
import time

# Load Objective-C runtime:
objc = cdll.LoadLibrary(util.find_library('objc'))
objc.sel_getName.restype = c_char_p
objc.sel_getName.argtypes = [c_void_p]
objc.sel_registerName.restype = c_void_p
objc.sel_registerName.argtypes = [c_char_p]
objc.objc_getClass.argtypes = [c_char_p]
objc.objc_getClass.restype = c_void_p

# Some helper methods:
def obj_to_str(obj):
	objc.objc_msgSend.argtypes = [c_void_p, c_void_p]
	objc.objc_msgSend.restype = c_void_p
	desc = objc.objc_msgSend(obj, objc.sel_registerName('description'))
	objc.objc_msgSend.argtypes = [c_void_p, c_void_p]
	objc.objc_msgSend.restype = c_char_p
	return objc.objc_msgSend(desc, objc.sel_registerName('UTF8String'))

def msg(obj, restype, sel, argtypes=None, *args):
	if argtypes is None:
		argtypes = []
	objc.objc_msgSend.argtypes =  [c_void_p, c_void_p] + argtypes
	objc.objc_msgSend.restype = restype
	res = objc.objc_msgSend(obj, objc.sel_registerName(sel), *args)
	return res

def cls(cls_name):
	return objc.objc_getClass(cls_name)

def nsstr(s):
	return msg(cls('NSString'), c_void_p, 'stringWithUTF8String:', [c_char_p], s)

def nsurl_from_path(s):
	return msg(cls('NSURL'), c_void_p, 'fileURLWithPath:', [c_void_p], nsstr(s))

def ns_int(i):
	return msg(cls('NSNumber'), c_void_p, 'numberWithInt:', [c_int], i)

def ns_float(f):
	return msg(cls('NSNumber'), c_void_p, 'numberWithFloat:', [c_float], f)

def main():
	AVAudioSession = cls('AVAudioSession')
	shared_session = msg(AVAudioSession, c_void_p, 'sharedInstance')
	category_set = msg(shared_session, c_bool, 'setCategory:error:', [c_void_p, c_void_p], nsstr('AVAudioSessionCategoryPlayAndRecord'), None)
	
	settings = msg(cls('NSMutableDictionary'), c_void_p, 'dictionary')
	kAudioFormatMPEG4AAC = 1633772320
	msg(settings, None, 'setObject:forKey:', [c_void_p, c_void_p], ns_int(kAudioFormatMPEG4AAC), nsstr('AVFormatIDKey'))
	msg(settings, None, 'setObject:forKey:', [c_void_p, c_void_p], ns_float(44100.0), nsstr('AVSampleRateKey'))
	msg(settings, None, 'setObject:forKey:', [c_void_p, c_void_p], ns_int(2), nsstr('AVNumberOfChannelsKey'))
	
	output_path = os.path.abspath('Recording.m4a')
	out_url = nsurl_from_path(output_path)
	recorder = msg(cls('AVAudioRecorder'), c_void_p, 'alloc')
	recorder = msg(recorder, c_void_p, 'initWithURL:settings:error:', [c_void_p, c_void_p, c_void_p], out_url, settings, None)
	started_recording = msg(recorder, c_bool, 'record')
	
	# https://forum.omz-software.com/topic/2178/save-audio-files-from-speech/10
	
	if started_recording:
		import speech, sound
		speech.say('Whatever you want it to say')
		#time.sleep(however many seconds long is the recording)
		#im not sure if say() is asynchronous, if so, uncomment last line
		msg(recorder, None, 'stop')
		msg(recorder, None, 'release')
		#sound.play_effect(os.abspath('Recording.m4a'))
		#uncomment last line if you want it to play again
		
	#if started_recording:
		#print 'Recording started, press the "stop script" button to end recording...'
	#try:
		#while True:
			#pass
	#except KeyboardInterrupt:
		#print 'Stopping...'
		#msg(recorder, None, 'stop')
		#msg(recorder, None, 'release')
		#print 'Stopped recording.'
		import console
		console.quicklook(os.path.abspath('Recording.m4a'))

if __name__ == '__main__':
	main()
