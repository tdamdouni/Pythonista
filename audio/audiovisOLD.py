# https://forum.omz-software.com/topic/2633/problem-with-johnbs-avaudiorecodre-class-under-actual-release

# https://github.com/jsbain/audiovis/blob/master/audiovis.py

# experiments with audio visualization in pythonista beta

'''
Audio Visualizer for puthonista beta

Uses ctypes to create AvAudioRecorder instance.  actually, creates multiple overlapping recorders, in order to provide higher update rate.

calling record() starts writing to a file.  calling stop() stops writing.  calling data() returns a scaled numpy array.  calling fft() is experimental, but returns scaled fft of the data.

since data can only be read after calling stop, and in fact, maybe quite some time after, multiple rcorders allows higher update rates.  basically, divide T into Nr slices:
      1) read data from r[0], then start r[0].  stop r[0+floor(Nr/2)]
      2) read date from r[1], then start r[1].  stop r[1 + floor(Nr/2)]
      etc
      thus, data is updated frequently, but we allow ample time for the recorder to stop before we read it.
      

'''
from __future__ import print_function
from ctypes import c_void_p, c_char_p, c_double, c_float, c_int, cdll, util, c_bool
import os
import time
import wave,array
import math
import numpy as np
import numpy.fft

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
class AVAudioSession(object):
   def __init__(self,sample_rate=8000.0):
      AVAudioSession = cls('AVAudioSession')
      shared_session = msg(AVAudioSession, c_void_p, 'sharedInstance')
      category_set = msg(shared_session, c_bool, 'setCategory:error:', [c_void_p, c_void_p], nsstr('AVAudioSessionCategoryPlayAndRecord'), None)

      settings = msg(cls('NSMutableDictionary'), c_void_p, 'dictionary')
      kAudioFormat = int('lpcm'.encode('hex'),16)

      msg(settings, None, 'setObject:forKey:', [c_void_p, c_void_p], ns_int(kAudioFormat), nsstr('AVFormatIDKey'))

      msg(settings, None, 'setObject:forKey:', [c_void_p, c_void_p], ns_float(sample_rate), nsstr('AVSampleRateKey'))

      msg(settings, None, 'setObject:forKey:', [c_void_p, c_void_p], ns_int(1), nsstr('AVNumberOfChannelsKey'))
      self.settings=settings
      self.shared_session=shared_session
      self.category_set=category_set
      self.AVAudioSession=AVAudioSession
class AVAudioRecorder(object):
   def __init__(self,idx=1):
      sess=AVAudioSession()
      self.output_path = os.path.abspath('recorder{}.wav'.format(idx))
      self.out_url = nsurl_from_path(self.output_path)
      self.recorder1 = msg(cls('AVAudioRecorder'), c_void_p, 'alloc')
      recorder = msg(self.recorder1, c_void_p, 'initWithURL:settings:error:', [c_void_p, c_void_p, c_void_p], self.out_url, sess.settings, None)
      self.recorder=recorder
      self.__msg=msg
      self.record()
      self.stop()
   def record(self):
      msg(self.recorder, c_bool, 'record')
   def stop(self):
      msg(self.recorder,None,'stop')
   def data(self):
      try:
         wf=wave.open(self.output_path)
         N=wf.readframes(wf.getnframes())
         y=array.array('h',N)
         wf.close()
      except IOError:
         y=array.array('h',[])
      #os.remove(output_path)
      return np.double(y)/2**15
   def fft(self):
      try:
         return -0.1+0.1*np.log10(abs(np.fft.fft(self.data()[0:2*W]*np.hanning(W*2),int(W*2))))[0:int(W)]
      except ValueError:
          return np.double([])
   def __del__(self):
      msg=self.__msg
      msg(self.recorder,None,'stop')
      msg(self.recorder, None, 'release')
      os.remove(self.output_path)
      
      
T=1.0 # recording length.  dont make too small, or recorder wont record.
Nr=5  # number of recorders.  this defines frame update time:mthe frame update will be is T/(Nr-1), though this may be driven slower by other factors 
r=[AVAudioRecorder(i) for i in xrange(Nr)]

Np=float(2001); # float..num points to plot on screen.. too high will lower frame rate
import ui
W,H=ui.get_screen_size()

if 1:

   import sk
   from threading import Thread
   class Vis(sk.Scene):
      def __init__(self,dofft=False):
         self.v=[sk.SpriteNode() for x in xrange(int(Np))]
         for i,sp in enumerate(self.v):
            sp.size=(1.5,1.5)
            sp.position=(float(i)/Np*W,H/2)
            sp.color=(1.0*i/Np,(1-1.0*i/Np),(0.5+i/2.0))
            self.add_child(sp)
         # first, start r[0]
         # then, 0.5 sec later, start r[1]
         # then, 0.5 sec later, start r[2], stop r[0]
         # read r[0], then start r[0], stop r[1]
         # basically, each frame we read/start one, and stop i+1
         self.a1=sk.Action.call(self.update_y)
         self.a2=sk.wait(T/(Nr-1))
         self.a3=sk.sequence([self.a1,self.a2])
         self.a4=sk.Action.repeat_forever(self.a3)
         n=sk.Node()
         n.name='n'
         self.add_child(n)
         n.run_action(self.a4)
         self.dofft=dofft
         self.idx=0
      def update_y(self):
         if self.dofft:
            y=r[self.idx%Nr].fft()
         else :
            y=r[self.idx%Nr].data()
         # start idx, stop idx+1
         r[self.idx%Nr].record()
         #stop recorder a few samples before im ready to read it
         lookaheadidx=self.idx+1+int(0.25//(T/(Nr-1)))
         r[lookaheadidx%Nr].stop()
         self.idx+=1

         if len(y)==0:
            return

         for i,n in enumerate(self.v):
            iy=int(i/Np*len(y))
            n.position=(i/Np*W,y[iy]*H+H/2)
      def did_stop(self):
         print('stopping')
         #raise Error()
         self['n'][0].remove_all_actions()
         [rec.stop() for rec in r]
         ui.delay(cleanup,0.25)
         # the scene seems to crash when restarting, unless we raise an error here
         raise KeyboardInterrupt

   
   #sc=Vis(dofft=True)
   sc=Vis(dofft=False)
   v=sk.View(sc)
   v.shows_fps=True
   v.shows_node_count=True
   v.present()
   
   def cleanup():
      # required b/c beta always clears globals
      print('cleaning up')
      del globals()['r']
      del globals()['sc']
      del globals()['v']