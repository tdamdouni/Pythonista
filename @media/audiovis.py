# https://github.com/jsbain/audiovis/blob/master/audiovis.py
print 'loading... please wait'
from ctypes import c_void_p, c_char_p, c_double, c_float, c_int, cdll, util, c_bool
import os
import time
import wave,array
import math
import numpy as np

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

def ns_double(d):
   return msg(cls('NSNumber'), c_void_p, 'numberWithDouble:', [c_double], d)
   

def record():
   '''record 1 sec of mic data, and return as a scaled numpy array.  this doesnt seem to work for < 1 sec'''
   AVAudioSession = cls('AVAudioSession')
   shared_session = msg(AVAudioSession, c_void_p, 'sharedInstance')
   category_set = msg(shared_session, c_bool, 'setCategory:error:', [c_void_p, c_void_p], nsstr('AVAudioSessionCategoryPlayAndRecord'), None)

   settings = msg(cls('NSMutableDictionary'), c_void_p, 'dictionary')
   kAudioFormat = int('lpcm'.encode('hex'),16)
   msg(settings, None, 'setObject:forKey:', [c_void_p, c_void_p], ns_int(kAudioFormat), nsstr('AVFormatIDKey'))
   msg(settings, None, 'setObject:forKey:', [c_void_p, c_void_p], ns_float(8000.0), nsstr('AVSampleRateKey'))
   msg(settings, None, 'setObject:forKey:', [c_void_p, c_void_p], ns_int(1), nsstr('AVNumberOfChannelsKey'))

   output_path = os.path.abspath('test.wav')
   out_url = nsurl_from_path(output_path)
   recorder = msg(cls('AVAudioRecorder'), c_void_p, 'alloc')
   recorder = msg(recorder, c_void_p, 'initWithURL:settings:error:', [c_void_p, c_void_p, c_void_p], out_url, settings, None)
   started_recording = msg(recorder, c_bool, 'record')
   import time
   T=1.0
   time.sleep(T)
   def stop():
      msg(recorder,None,'stop')
      msg(recorder, None, 'release')
      wf=wave.open(output_path)
      y=array.array('h',wf.readframes(wf.getnframes()))
      wf.close()
      return y
   y=stop()
   return np.double(y)/2**15 #np.log10(np.abs(np.fft.fftshift(np.fft.fft(np.double(y)))))/20
print 'just a sec'
import ui
W=ui.get_screen_size().width
H=ui.get_screen_size().height
import sk
class Vis(sk.Scene):
   def __init__(self):
      self.v=[sk.SpriteNode() for x in xrange(int(W)*2)]
      for i,sp in enumerate(self.v):
         sp.size=(5,5)
         sp.position=(i/2.,H/2)
         sp.color=(i/W/2,(1-i/W/2),(0.5+i/800.0))
         self.add_child(sp)
      self.a1=sk.Action.call(self.update_y)
      self.a2=sk.wait(0.1)
      self.a3=sk.sequence([self.a1,self.a2])
      self.a4=sk.Action.repeat_forever(self.a3)
      n=sk.Node()
      self.add_child(n)
      n.run_action(self.a4)
   def update_y(self):
      y=record()
      for i,n in enumerate(self.v):
         iy=int(i/W/2.0*len(y))
         n.position=(i/2.,y[iy]*H+H/2)
   

v=sk.View(Vis())
v.present()