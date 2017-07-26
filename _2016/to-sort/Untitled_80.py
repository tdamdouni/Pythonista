# https://gist.github.com/jsbain/c595e7360d6b2d6ca903f3b909b6bece

from objc_util import *
s=ObjCClass('NSInputStream')

from ctypes import *
from objc_util import *


c.CFStreamCreatePairWithSocketToHost.argtypes=[c_void_p,c_void_p,c_int32,POINTER(c_void_p),POINTER(c_void_p)]


def CFStreamCreatePairWithSocketToHost(host, port):
	readStream = c_void_p(0)
	writeStream = c_void_p(0)
	#url=nsurl(host)
	c.CFStreamCreatePairWithSocketToHost(None, (host), port, byref(readStream), byref(writeStream))
	
	return (ObjCInstance(readStream), ObjCInstance(writeStream))
	
inputBuffer=create_string_buffer(2048)
def stream_handleEvent_(_self,_cmd, stream, event):
	print(ObjCInstance(stream),event)
	streamobj=ObjCInstance(stream)
	try:
		if streamobj.hasBytesAvailable():
			l=streamobj.read_maxLength_(inputBuffer,len(inputBuffer))
			print(inputBuffer.value[0:l])
	except AttributeError:
		pass
		
myStreamDelegate=create_objc_class('MyStreamDelegate', methods=[stream_handleEvent_], protocols=['NSStreamDelegate'])
d=myStreamDelegate.alloc()
host=ns('192.168.0.1')
(readstream,writestream)=CFStreamCreatePairWithSocketToHost(host,80)
readstream.delegate=d
writestream.delegate=d
kCFRunLoopDefaultMode=ObjCInstance(c_void_p.in_dll(c,'kCFRunLoopDefaultMode'))
crl=ObjCClass('NSRunLoop').currentRunLoop()
readstream.scheduleInRunLoop_forMode_(crl,kCFRunLoopDefaultMode)
writestream.scheduleInRunLoop_forMode_(crl,kCFRunLoopDefaultMode)
readstream.open()
writestream.open()

