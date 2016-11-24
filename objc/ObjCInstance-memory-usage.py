# -*- coding: utf-8 -*-

# https://gist.github.com/jsbain/b926b5cbc1b7c7d5b2a94cf41dd8ec4c

# https://forum.omz-software.com/topic/3674/objcinstance-eat-memory/13

from objc_util import *
import ctypes,time,os,struct,array,console

def getfile():
	import os
	import requests
	if not os.path.exists('Allegro.mp3'):
		r=requests.get('http://www.stephaniequinn.com/Music/Allegro%20from%20Duet%20in%20C%20Major.mp3')
		with open('Allegro.mp3','bw') as f:
			f.write(r.content)
getfile()
bufsize = 4410                              # Audio Tap out
input_type = 2
play_filename ='Allegro.mp3'
global Srv_Ctime,dWhen
Srv_Ctime,dWhen = 0,0

#
# Get iOS System Memory Info
#
NSProcessInfo = ObjCClass('NSProcessInfo')
NSByteCountFormatter = ObjCClass('NSByteCountFormatter')
class c_vm_statistics(Structure):
	_fields_ = [('free_count', c_uint),
	('active_count', c_uint),
	('inactive_count', c_uint),
	('wire_count', c_uint),
	('zero_fill_count', c_uint),
	('reactivations', c_uint),
	('pageins', c_uint),
	('pageouts', c_uint),
	('faults', c_uint),
	('cow_faults', c_uint),
	('lookups', c_uint),
	('hits', c_uint),
	('purgeable_count', c_uint),
	('purges', c_uint),
	('speculative_count', c_uint)]
c = ctypes.cdll.LoadLibrary(None)
mach_host_self = c.mach_host_self
mach_host_self.restype = c_uint
mach_host_self.argtypes = [c_void_p]
host_page_size = c.host_page_size
host_page_size.restype = c_int
host_page_size.argtypes = [c_uint, POINTER(c_uint)]
host_statistics = c.host_statistics
host_statistics.restype = c_int
host_statistics.argtypes = [c_uint, c_int, POINTER(c_int), POINTER(c_uint)]
host_port = c_uint()
host_size = c_uint()
page_size = c_uint()
host_port = mach_host_self(None)
host_size = c_uint(int(sizeof(c_vm_statistics) / sizeof(c_int)))
host_page_size(host_port, byref(page_size))
vm_stat = c_vm_statistics()
HOST_VM_INFO = c_int(2) # This is a c macro

# Return System Used/Free memory (bytes)
def Get_mem():
	get_host_statistics = host_statistics(host_port, HOST_VM_INFO, ctypes.cast(byref(vm_stat),ctypes.POINTER(c_int)), ctypes.byref(host_size))
	mem_used = (vm_stat.active_count + vm_stat.inactive_count + vm_stat.wire_count) * int(page_size.value)
	mem_free = vm_stat.free_count * int(page_size.value)
	return mem_used,mem_free
	
# Get System Time
curTime = ctypes.cdll.LoadLibrary(None)
curTime.CACurrentMediaTime.restype=c_double

# AVAudio Define
AVAudioEngine=ObjCClass('AVAudioEngine')
AVAudioSession=ObjCClass('AVAudioSession')
AVAudioPlayerNode=ObjCClass('AVAudioPlayerNode')
AVAudioFile=ObjCClass('AVAudioFile')
AVAudioUnitEQ=ObjCClass('AVAudioUnitEQ')
AVAudioMixerNode=ObjCClass('AVAudioMixerNode')
AVAudioPCMBuffer=ObjCClass('AVAudioPCMBuffer')
AVAudioFormat=ObjCClass('AVAudioFormat')
AVAudioUnitEQFilterParameters=ObjCClass('AVAudioUnitEQFilterParameters')
AVAudioSessionPortDescription=ObjCClass('AVAudioSessionPortDescription')
#AVAudioCompressedBuffer=ObjCClass('AVAudioCompressedBuffer')
#AVAudioConverter=ObjCClass('AVAudioConverter')
AVAudioTime=ObjCClass('AVAudioTime')
class AudioStreamBasicDescription(ctypes.Structure):
	_fields_=[('mSampleRate',ctypes.c_double),('mFormatID',ctypes.c_uint32),('mFormatFlags',ctypes.c_uint32),('mBytesPerPacket',ctypes.c_uint32),('mFramesPerPacket',ctypes.c_uint32),('mBytesPerFrame',ctypes.c_uint32),('mChannelsPerFrame',ctypes.c_uint32),('mBitsPerChannel',ctypes.c_uint32),('mReserved',ctypes.c_uint32)]
	
# create AVAudio engine
def setup():
	error=ctypes.c_void_p(0)
	session=AVAudioSession.sharedInstance()
	session.setCategory('AVAudioSessionCategoryPlayAndRecord',error=ctypes.pointer(error))
	
	if error:
		raise Exception('error setting up category')
	session.setActive(True, error=ctypes.pointer(error))
	if error:
		raise Exception('error setting up session active')
	engine=AVAudioEngine.new()
	return engine
	
#
# Audio Tap
#
def processBuffer(self,buffer,when,cmd):
	global Srv_Ctime,dWhen
	
	# Record audio when time
	t_when = AVAudioTime.secondsForHostTime(ObjCInstance(when).hostTime())
	# Record audio tap out time,and conver to 8 bytes
	Srv_Ctime = curTime.CACurrentMediaTime()
	dWhen = Srv_Ctime - t_when
	
	# get buffer
	cbuf = ObjCInstance(buffer)
	# ios 9 need this line,because installTapOnBus buffsize not effect,but ios 10 it's work.
	cbuf.frameLength = bufsize
	cbuf._cached_methods.clear()
	cbuf=[]
	
process_block=ObjCBlock(processBuffer,restype=None,argtypes=[c_void_p,c_void_p,c_void_p,c_void_p])


#
# Audio Init
#
# open a mp3 player
fileurl = nsurl(os.path.abspath(play_filename))
file = AVAudioFile.alloc().initForReading_error_(fileurl,None)
bd=file.processingFormat().streamDescription()
# AVAudioFormat: 0-other,1-PCM float32,2 PCM float64,3-PCM int16,4-PCM int32
#audioFormat=AVAudioFormat.alloc().initWithCommonFormat_sampleRate_channels_interleaved_(1,44100,2,False)
audioFormat = file.processingFormat()
# save file to buffer for loop player
audioFrameCount = file.length()
audioFileBuffer = AVAudioPCMBuffer.alloc().initWithPCMFormat_frameCapacity_(audioFormat,audioFrameCount)
file.readIntoBuffer_error_(audioFileBuffer,None)
# init Audio Engine
engine=setup()
# Mic
ainput = engine.inputNode()
# Player for mp3
player = AVAudioPlayerNode.new()
engine.attachNode(player)
# loop play audio files (so need using buff)
#player.scheduleFile_atTime_completionHandler_(file,None,None)
player.scheduleBuffer_atTime_options_completionHandler_(audioFileBuffer,None,1,None)
# Mixer
mixer = engine.mainMixerNode()
# Connect devices
if input_type == 1 or input_type == 3:
	engine.connect_to_format_(ainput,mixer,ainput.inputFormatForBus_(0))
if input_type == 2 or input_type == 3:
	engine.connect_to_format_(player,mixer,audioFormat)
# install Tap on mixer
mixer.installTapOnBus(0,bufferSize=bufsize,format=audioFormat,block=process_block)
print('###### starting#####')
# start audio engin
engine.prepare()
engine.startAndReturnError_(None)
# play mp3 music


# UI Display Loop
ui_cnt = 0
try:
	while 1:
		time.sleep(0.05)
		ui_cnt += 1
		mem_used,mem_free = Get_mem()
		if ui_cnt==100:
			if input_type == 2 or input_type ==3:
				print('playing')
				player.play()
		if (ui_cnt % 10) == 0:
			print( 'Memory used:','{:,} K delaT={}'.format(mem_used/1024,dWhen))
except KeyboardInterrupt:
	print('#stopping engine')
	engine.pause()

