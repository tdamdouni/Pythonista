# https://forum.omz-software.com/topic/4165/amazon-lex-using-audiorecorder/7

from objc_util import *
import boto3
import os
import sound
import console
import uuid

def record(file_name):
	AVAudioSession = ObjCClass('AVAudioSession')
	NSURL = ObjCClass('NSURL')
	AVAudioRecorder = ObjCClass('AVAudioRecorder')
	shared_session = AVAudioSession.sharedInstance()
	category_set = shared_session.setCategory_error_(ns('AVAudioSessionCategoryPlayAndRecord'), None)
	
	settings = {
	ns('AVFormatIDKey'): ns(1819304813),
	ns('AVSampleRateKey'):ns(16000.0),
	ns('AVNumberOfChannelsKey'):ns(1),
	ns('AVLinearPCMBitDepthKey'):ns(16),
	ns('AVLinearPCMIsFloatKey'):ns(False),
	ns('AVLinearPCMIsBigEndianKey'):ns(False)
	}
	
	output_path = os.path.abspath(file_name)
	out_url = NSURL.fileURLWithPath_(ns(output_path))
	recorder = AVAudioRecorder.alloc().initWithURL_settings_error_(out_url, settings, None)
	if recorder is None:
		console.alert('Failed to initialize recorder')
		return None
		
	started_recording = recorder.record()
	if started_recording:
		print('Recording started, press the "stop script" button to end recording...')
	try:
		while True:
			pass
	except KeyboardInterrupt:
		print('Stopping...')
		recorder.stop()
		recorder.release()
		print('Stopped recording.')
	return output_path
	
	
def main():
	console.clear()
	
	path = record("{}.pcm".format(uuid.uuid4().hex))
	
	if path is None:
		print('Nothing recorded')
		return
		
	sound.play_effect(path)
	
	recording = open(path, 'rb')
	session = boto3.Session(profile_name='lex')
	client = session.client('lex-runtime')
	
	r = client.post_content(botName='BookTrip', botAlias='$LATEST', userId=uuid.uuid4().hex,
	contentType='audio/l16; rate=16000; channels=1',
	accept='text/plain; charset=utf-8',
	inputStream=recording)
	print(r)
	
	os.remove(path)
	
if __name__ == '__main__':
	main()

