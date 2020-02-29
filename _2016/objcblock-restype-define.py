# -*- coding: utf-8 -*-
#!python2

# https://forum.omz-software.com/topic/3741/objcblock-restype-define-question/9

from __future__ import print_function
from objc_util import *
import ctypes,time,os,struct,array,console

# AVAudio Define
AVAudioEngine=ObjCClass('AVAudioEngine')
AVAudioSession=ObjCClass('AVAudioSession')
AVAudioUnit=ObjCClass('AVAudioUnit')
AVAudioPlayerNode=ObjCClass('AVAudioPlayerNode')
AVAudioFile=ObjCClass('AVAudioFile')
AVAudioPCMBuffer=ObjCClass('AVAudioPCMBuffer')
AVAudioUnitEffect=ObjCClass('AVAudioUnitEffect')
AVAudioFormat=ObjCClass('AVAudioFormat')
AVAudioCompressedBuffer=ObjCClass('AVAudioCompressedBuffer')
AVAudioConverter=ObjCClass('AVAudioConverter')


# AVAudioFormat: 0-other,1-PCM float32,2 PCM float64,3-PCM int16,4-PCM int32
informat = AVAudioFormat.alloc().initWithCommonFormat_sampleRate_channels_interleaved_(3,44100,2,False) 
outformat = AVAudioFormat.alloc().initWithSettings_(ns({'AVSampleRateKey':44100,'AVNumberOfChannelsKey':2,'AVFormatIDKey':struct.unpack('I', b' caa')[0]})) # ,'mFramesPerPacket':1024}))

inBuffer = AVAudioPCMBuffer.alloc().initWithPCMFormat_frameCapacity_(informat,4096)
converter = AVAudioConverter.alloc().initFromFormat_toFormat_(informat,outformat)
outBuffer = AVAudioCompressedBuffer.alloc().initWithFormat_packetCapacity_maximumPacketSize_(outformat, 8,converter.maximumOutputPacketSize())

gcnt = 0

# typedef AVAudioBuffer * _Nullable (^AVAudioConverterInputBlock)(AVAudioPacketCount inNumberOfPackets, AVAudioConverterInputStatus *outStatus);
def conv_block(self,inNumberOfPackets,buffstat):
    global gcnt
    
    # buffstat: 0-have data 1-no data 2-endOfStream   3-error
    print('@1',inNumberOfPackets,buffstat.contents.value)
    gcnt += 1
    if gcnt == 1:
        buffstat.contents.value = 0
        print('@2',inNumberOfPackets,buffstat.contents.value)
        print('!!! InBuff:',inBuffer,type(inBuffer),ctypes.cast(inBuffer,ctypes.c_void_p)) #,ctypes.addressof(inBuffer)
        return None #pointer(c_void_p(inBuffer.ptr))
    else:
        buffstat.contents.value = 2
        return None
        
#convblock=ObjCBlock(conv_block,restype=POINTER(c_void_p),argtypes=[c_void_p,c_int32,POINTER(c_long)])
convblock=ObjCBlock(conv_block,restype=c_void_p,argtypes=[c_void_p,c_int32,POINTER(c_long)])

error=ctypes.c_void_p(0)

status = converter.convertToBuffer_error_withInputFromBlock_(outBuffer,error,convblock)
print('>>Ret1:',status)
print('>>out1:',outBuffer)
if error:
    print('>>Err:',ObjCInstance(error))

status = converter.convertToBuffer_error_withInputFromBlock_(outBuffer,None,convblock)
print('>>Ret2:',status)
print('>>out2:',outBuffer)


# --------------------
