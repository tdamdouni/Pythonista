# coding: utf-8

# version 1.5

# https://github.com/jsbain/uicomponents/blob/master/SPLView11.py

# view spl data files in zoomable interactive view

import ui

# beta workaround
import sys
if '.' not in sys.path:
   sys.path.append('.')

# for plotting and transformations
from matplotlib import pyplot as plt 
from matplotlib.transforms import Bbox, BboxTransformTo,BboxTransform

#numpy
np=plt.np

# for threading.Lock
import threading

import ZoomSlider
reload(ZoomSlider)
from ZoomSlider import ZoomSlider
import uidir


# debugging
import io, logging
reload(logging)
import io
from StringIO import StringIO


### Debugging logger as a StringIO object
logger = logging.getLogger('basic_logger')
logger.setLevel(logging.DEBUG)
log_capture_string = StringIO()
ch = logging.StreamHandler(log_capture_string)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(funcName)s- %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def printLog():
   ### Pull the contents back into a string and close the stream
   global log_capture_string
   log_contents = log_capture_string.getvalue()
   log_capture_string.close()
   log_capture_string = StringIO()
   logger.handlers[0].stream=log_capture_string
   print(log_contents.lower())


## run a runction in an async thread.  better than ui.in_background for this application, because it is not queued up
def run_async(func):
   from threading import Thread
   from functools import wraps

   @wraps(func)
   def async_func(*args, **kwargs):
      func_hl = Thread(target = func, args = args, kwargs = kwargs)
      func_hl.start()
      return func_hl

   return async_func

## main class
class SPLView(ui.View):  
   def __init__(self, N_onscreen=700,*args, **kwargs):
      ui.View.__init__(self,*args,**kwargs)
      # ready lock is used to protect calls to matplotlib
      self.ready=threading.Lock()
      #set up zoomable sliders
      self.hslider=ZoomSlider(frame=(self.width*0.08,0,self.width*0.84,self.height*0.08),vert=0,flex='wt')
      self.vslider=ZoomSlider(frame=(0,self.height*0.08,self.width*0.08,self.height*0.84),vert=1,flex='hr')
      self.add_subview(self.hslider)
      self.add_subview(self.vslider)
      self.hslider.barvalue=0.125
      self.hslider.barwidth=0.25
      self.vslider.barvalue=0.5
      self.vslider.barwidth=1.0
      self.hslider.action=self.did_slide
      self.vslider.action=self.did_slide
      #matplotlib image output
      self.img_view = ui.ImageView(frame=[self.width*0.08,self.height*0.08,self.width*0.84,self.height*0.84],flex='WH',bg_color=(1,1,1))
      self.add_subview(self.img_view)
      # image buffer
      self.b = io.BytesIO()

      #store base xlim and ylim, only update when drag ends
      self.xlim=plt.xlim()
      self.ylim=plt.ylim()
      self.N_onscreen=N_onscreen # number of points onscreen
 
      # fast and slow dpi..  set low_dpi to lower number for snappier response
      self.high_dpi=92
      self.low_dpi=16.
      self.device_dpi=72
      # set output image size to match view size.  this probably should be modified to use actual device dpi and size.  fonts and line width are based on pts, not pixels
      plt.gcf().set_size_inches(self.img_view.width/self.device_dpi,self.img_view.height/self.device_dpi)
      #update plot, ensuring update really happens
      #self.update_plt(dpi=self.high_dpi, waitForLock=True)

      #ObjCInstance(self).becomeFirstResponder()
   def layout(self):      
      '''ensures that figure is plotted at correct aspct ratio'''
      plt.gcf().set_size_inches(self.img_view.width/self.device_dpi,self.img_view.height/self.device_dpi)
      self.update_plt(dpi=self.high_dpi, waitForLock=True)

   @run_async
   def update_plt(self,dpi=163,waitForLock=False):
      '''re-draw the plot in a background thread
      set dpi low for fast drawing. 
      if waitForLock is False, and lock cannot be aquired (already rendering), then return immediately.  otherwise, wait (i.e when motion has ended, and we want to guarantee an image is generated)       
      TODO: use pan/pinch velocity to control the dpi.      
      '''     
      if waitForLock:
         self.ready.acquire()
      try:
         # set axes limits
         lims=self.compute_lims()
         plt.xlim(lims[0])
         plt.ylim(lims[1])     
         self.update_plot_data()
         # render image
         self.b.seek(0)   
         plt.savefig(self.b,format='jpg',dpi=dpi)
         self.img_view.image = ui.Image.from_data(self.b.getvalue())
      finally:
         try:
            self.ready.release()         
         except:
            pass
           
   def update_plot_data(self):
      '''update the data in the current plot, by resampling.
      If the number of datapoints within the current xlim is higher than N_onscreen, compute peak over a resampled window, and log average as the "slow" data'''
      idx=[max(min(int(x*N/24),N),0) for x in plt.xlim()]
      decimation_factor=max((idx[1]-idx[0])/self.N_onscreen,1)
      idx[1]=idx[0]+decimation_factor*self.N_onscreen 
      t=np.linspace(*(plt.xlim()+(self.N_onscreen,)))

      data_downsampled_pk=data[idx[0]:idx[1],1].reshape(self.N_onscreen,-1).max(1)
      
      data_downsampled_logmean=10.0*np.log10((10**(data[idx[0]:idx[1],0].reshape(self.N_onscreen,-1)/10.0)).mean(1))    
     
      ax.lines[0].set_data(t,data_downsampled_pk)
      ax.lines[1].set_data(t,data_downsampled_logmean)
      plt.title('Decimation factor={}'.format(decimation_factor))
   def scale_ended(self,scale):
      '''called when scaling is complete'''
      self.motion_ended()

   def pan_ended(self,pan):
      '''called when scaling is complete'''
      self.motion_ended()      
      
   def compute_lims(self):
      '''compute new axes limits based on pan/zoom.
         basically, get limits in terms of bbox of size 1.  
         transform to bbox of size orig lims.       
      '''
      xlnorm=      self.hslider.barvalue+np.array([-.5,.5])*self.hslider.barwidth
      ylnorm=      self.vslider.barvalue+np.array([-.5,.5])*self.vslider.barwidth
      viewBbox=Bbox(zip(xlnorm,ylnorm))
      limBB=Bbox(zip(self.xlim,self.ylim))
      newlims=Bbox(BboxTransformTo(limBB).transform(viewBbox))
      return [(newlims.x0,newlims.x1),(newlims.y0,newlims.y1)]

   def motion_ended(self):
      '''called when motion ends.  clean up scale/pan parms, and render final version'''
      logger.debug('motion end')
      #render with high dpi
      self.update_plt(dpi=self.high_dpi,waitForLock=True)
   def did_slide(self,sender):
      if sender.dragging:
         self.update_transform()
      else:
         self.motion_ended()
   def update_transform(self):
      '''if lock can be acquired, start rendering thread, otherwise return.
      TODO:  while rendering, just update .transform.  update_plt would need to reset .transform'''
      
      if self.ready.acquire(False):
         self.update_plt(dpi=self.low_dpi)

if __name__=='__main__':
   v=ui.View(frame=(0,0,700,700))

   plt.close('all')
   
   if globals().get('data') is None:
      filename=uidir.getFile()
      data = np.fromfile(filename, dtype=np.float32).reshape(-1, 2)

   data[data<=0]=33.33 # clean
   N=len(data)

   t0=np.linspace(0,24,N)

   fig = plt.figure()
   ax = fig.add_subplot(1, 1, 1)

   ax.plot(0, 0,marker='.')
   ax.hold(True)
   ax.plot(0, 0,marker='.',c='r')    
   plt.hold(False)
   plt.title('SPLnFFT Noise data') 
   plt.xlim((0,24))
   plt.ylim((33,90))
   plt.xlabel('time (hrs)')
   plt.ylabel('dB')
   plt.legend(('Peak','Average'))
   m=SPLView(frame=v.bounds,flex='wh')
   v.add_subview(m)

   v.present('fullscreen')