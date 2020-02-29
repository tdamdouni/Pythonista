# https://github.com/jsbain/audiovis/blob/master/audiovis.py

# https://forum.omz-software.com/topic/2633/problem-with-johnbs-avaudiorecodre-class-under-actual-release

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
from objc_util import *
import os
import time
import wave,array
import math
import numpy as np
import numpy.fft
import scene



# Some helper methods:
AVAudioSession = ObjCClass('AVAudioSession')
class AVAudioSessionWrapper(object):
   def __init__(self,sample_rate=8000.0):
      shared_session = AVAudioSession.sharedInstance()
      category_set = shared_session.setCategory_error_('AVAudioSessionCategoryPlayAndRecord', None)
      kAudioFormat = int('lpcm'.encode('hex'),16)
      settings={'AVFormatIDKey':kAudioFormat,
						'AVSampleRateKey':sample_rate,
						'AVNumberOfChannelsKey':1}

      self.settings=settings
      self.shared_session=shared_session
      self.category_set=category_set
      
class AVAudioRecorderWrapper(object):
   def __init__(self,idx=1):
      sess=AVAudioSessionWrapper()
      self.output_path = os.path.abspath('recorder{}.wav'.format(idx))
      self.out_url = nsurl(self.output_path)
      #self.recorder1 = ObjCClass('AVAudioRecorder').alloc()
      self.recorder=ObjCClass('AVAudioRecorder').alloc().initWithURL_settings_error_(self.out_url, sess.settings, None)
      self.record()
      self.stop()
   def record(self):
   	self.recorder.record()
   def stop(self):
   	self.recorder.stop()
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
      import os
      self.recorder.stop()
      self.recorder.release()
      self.recorder=None
      os.remove(self.output_path)
      
      
T=1.0 # recording length.  dont make too small, or recorder wont record.
Nr=5  # number of recorders.  this defines frame update time:mthe frame update will be is T/(Nr-1), though this may be driven slower by other factors 
r=[AVAudioRecorderWrapper(i) for i in xrange(Nr)]

Np=float(2001); # float..num points to plot on screen.. too high will lower frame rate
import ui
W,H=ui.get_screen_size()

if 1:

   #import sk
   from threading import Thread
   class Vis(scene.Scene):
      def __init__(self,dofft=False):
         self.v=[scene.SpriteNode() for x in xrange(int(Np))]
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
         self.a1=scene.Action.call(self.update_y)
         self.a2=scene.Action.wait(T/(Nr-1))
         self.a3=scene.Action.sequence([self.a1,self.a2])
         self.a4=scene.Action.repeat(self.a3,-1)
         n=scene.Node()
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
   sc.shows_fps=True
   sc.shows_node_count=True
   scene.run(sc)