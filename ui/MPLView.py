# coding: utf-8

# version 1.6 Beta 

# ObjC

# https://github.com/jsbain/objc_hacks/blob/master/MPLView.py

# experiments with gestureRecognizers
# note this code may not work with 64bit code, due to bool encoding

import ui
from objc_util import *
import weakref
import io
from matplotlib import pyplot as plt 
from matplotlib.transforms import Bbox, BboxTransformTo,BboxTransform
np=plt.np
import time

import logging
reload(logging)
import io
from StringIO import StringIO
import threading

### Create the logger
logger = logging.getLogger('basic_logger')
logger.setLevel(logging.DEBUG)

### Setup the console handler with a StringIO object
log_capture_string = StringIO()
ch = logging.StreamHandler(log_capture_string)
ch.setLevel(logging.DEBUG)

### Optionally add a formatter
formatter = logging.Formatter('%(asctime)s - %(funcName)s- %(message)s')
ch.setFormatter(formatter)

### Add the console handler to the logger
logger.addHandler(ch)


def printLog():
   ### Pull the contents back into a string and close the stream
   global log_capture_string
   log_contents = log_capture_string.getvalue()
   log_capture_string.close()
   log_capture_string = StringIO()
   logger.handlers[0].stream=log_capture_string
   ### Output as lower case to prove it worked. 
   print(log_contents.lower())

def run_async(func):
   from threading import Thread
   from functools import wraps

   @wraps(func)
   def async_func(*args, **kwargs):
      func_hl = Thread(target = func, args = args, kwargs = kwargs)
      func_hl.start()
      return func_hl

   return async_func

# Create a new Objective-C class to act as the gesturerecognizer delegate...
try:
   # If the script was run before, the class already exists.
   GRDelegate = ObjCClass('GRDelegate')
except:
   IMPTYPE = ctypes.CFUNCTYPE(c_char, c_void_p, c_void_p, c_void_p,c_void_p)
   def gestureRecognizer_shouldRecognizeSimultaneouslyWithGestureRecognizer_imp(self, cmd, gr, other_gr):
      return chr(1)
     
   imp = IMPTYPE(gestureRecognizer_shouldRecognizeSimultaneouslyWithGestureRecognizer_imp)
   # This is a little ugly, but we need to make sure that `imp` isn't garbage-collected:
   ui._retain_gr_delegate = imp
   NSObject = ObjCClass('NSObject')
   class_ptr = c.objc_allocateClassPair(NSObject.ptr, 'GRDelegate', 0)
   selector = sel('gestureRecognizer:shouldRecognizeSimultaneouslyWithGestureRecognizer:')
   c.class_addMethod(class_ptr, selector, imp, 'c0@0:0@0@0')
   c.objc_registerClassPair(class_ptr)
   GRDelegate = ObjCClass('GRDelegate')

class PinchView(ui.View):
   def __init__(self, *args, **kwargs):
      ui.View.__init__(self, *args, **kwargs)
      self.pinchgesture_recognizer_target = ui.Button()
      self.pinchgesture_recognizer_target.action = self.did_pinch
      
      self.pangesture_recognizer_target = ui.Button()
      self.pangesture_recognizer_target.action = self.did_pan
      
      self.gr_delegate=GRDelegate.alloc().init().autorelease()
      self.recognizers={}
      self_objc = ObjCInstance(self)     
      pinchobjctarget=ObjCInstance(self.pinchgesture_recognizer_target)
      panobjctarget=ObjCInstance(self.pangesture_recognizer_target)
 
      pinchrecognizer = ObjCClass('UIPinchGestureRecognizer').alloc()
      self.recognizers['pinch'] =         pinchrecognizer.initWithTarget_action_( pinchobjctarget, sel('invokeAction:')).autorelease()

      
      panrecognizer = ObjCClass('UIPanGestureRecognizer').alloc()
      self.recognizers['pan'] =            panrecognizer.initWithTarget_action_( panobjctarget, sel('invokeAction:')).autorelease()
      self.recognizers['pan'].setMinimumNumberOfTouches_(2)
      
      for r in self.recognizers.values():
         self_objc.addGestureRecognizer_(r)
         r.setDelegate_(self.gr_delegate)
      self.panx,self.pany,self.sx,self.sy=0,0,1,1
      self.panx0,self.pany0,self.sx0,self.sy0=0,0,1,1
   def did_pan(self,sender):
      state=self.recognizers['pan'].state()
      pan=self.recognizers['pan'].translationInView_( self.recognizers['pan'].view())

      
      self.panx=pan.x
      self.pany=pan.y
      logger.debug(u'pan {} {} {}'.format(pan.x,pan.y,state))
      self.update_transform()
      if state==3:
         self.pan_ended(None)
   def pan_ended(self,pan):
         self.panx0+=self.panx
         self.pany0+=self.pany
         self.panx,self.pany=0,0
   def update_transform(self):
      self.transform=ui.Transform.concat(ui.Transform.translation(self.panx+self.panx0,self.pany+self.pany0),ui.Transform.scale(self.sx*self.sx0,self.sy*self.sy0))

   def did_pinch(self,sender):
      #print 'pinch'
      state=self.recognizers['pinch'].state()
      scale=self.recognizers['pinch'].scale()
      if state==1:
         self.scale_began(scale)
      elif state==2:
         self.scale_changed(scale)
      else:# state==3:
         self.scale_ended(scale)
      logger.debug(u'pinch {} {}'.format(scale,state))
   def scale_began(self,scale):
      self_objc = ObjCInstance(self)
      if self.recognizers['pinch'].numberOfTouches()<2:
         return
      self.centroid=[getattr(self.recognizers['pinch'].locationInView_(self.recognizers['pinch'].view()),axis) for axis in ('x','y')]
      self.centroid[0]-=self.panx
      self.centroid[1]-=self.pany
      touches=[ self.recognizers['pinch'].locationOfTouch_inView_( ctypes.c_uint(i), self.recognizers['pinch'].view() ) for i in (0,1)]
      dx=abs(touches[0].x-touches[1].x)
      dy=abs(touches[0].y-touches[1].y)
      if dy>3.0*dx:
         #vert
         pass
      elif dx>3.0*dy:
         #horiz
         pass
      else:
         pass

   def scale_changed(self,scale):
      self_objc = ObjCInstance(self)
      if self.recognizers['pinch'].numberOfTouches()<2:
         return
      self.centroid=[getattr(self.recognizers['pinch'].locationInView_(self.recognizers['pinch'].view()),axis) for axis in ('x','y')]
      self.centroid[0]-=self.panx
      self.centroid[1]-=self.pany
      touches=[ self.recognizers['pinch'].locationOfTouch_inView_( ctypes.c_uint(i), self.recognizers['pinch'].view() ) for i in (0,1)]
      dx=abs(touches[0].x-touches[1].x)
      dy=abs(touches[0].y-touches[1].y)
      if dy>3.0*dx:
         sx,sy=1.0,scale
         pass
      elif dx>3.0*dy:
         sx,sy=scale,1.0
         pass
      else:
         sx,sy=scale,scale
      self.sx=sx
      self.sy=sy
      #ui.animate(self.update_transform,0)
      self.update_transform()
   def scale_ended(self,scale):
      self.sx0*=self.sx
      self.sy0*=self.sy
      self.sx,self.sy=1,1
      #pass#print 'pinch end'

class MPLView(PinchView):  
   def __init__(self, *args, **kwargs):
      PinchView.__init__(self,*args,**kwargs)
      # prevent resize from causing redraw until we r ready
      self.ready=threading.Lock()
      #self.ready.acquire()
      
      self.img_view = ui.ImageView(frame=self.bounds,flex='WH')
      self.add_subview(self.img_view)
      self.b = io.BytesIO()

      #store base xlim and ylim, only update when drag ends
      self.xlim=plt.xlim()
      self.ylim=plt.ylim()
      self.centroid=tuple(self.center) # zoom center
 
      # fast and slow dpi.. 
      self.high_dpi=72.0
      self.low_dpi=16
      # set output image size to match view size.  this probably should be modified to use actual device dpi and size.  fonts and line width are based on pts, not pixels
      plt.gcf().set_size_inches(self.width/self.high_dpi,self.height/self.high_dpi)
      #update plot, ensuring update really happens
      self.update_plt(dpi=self.high_dpi, waitForLock=True)

      ObjCInstance(self).becomeFirstResponder()
   def layout(self):      
      '''ensures that figure is plotted at correct aspct ratio'''
      plt.gcf().set_size_inches(self.width/self.high_dpi,self.height/self.high_dpi)
      self.update_plt(dpi=self.high_dpi, waitForLock=True)

   @run_async
   def update_plt(self,dpi=163,waitForLock=False):
      '''re-draw the plot in a background thread
      set dpi low for fast drawing. 
      if waitForLock is False, and lock cannot be aquired (already rendering), then return immediately.  otherwise, wait (i.e when motion has ended)       
      TODO: use pan/pinch velocity to control the dpi.      
      '''     
      if waitForLock:
         self.ready.acquire()
      try:
         # set axes limits
         lims=self.compute_lims()
         plt.xlim(lims[0])
         plt.ylim(lims[1])     
         # render image
         self.b.seek(0)   
         plt.savefig(self.b,format='jpg',dpi=dpi)
         self.img_view.image = ui.Image.from_data(self.b.getvalue())
      finally:
         try:
            self.panx0=self.pany0=0
            self.sx0=1./self.sx
            self.sy0=1./self.sy
            self.img_view.transform=ui.Transform()
            
            self.ready.release()
            
         except:
            pass
           
         
   def scale_ended(self,scale):
      '''called when scaling is complete'''
      self.motion_ended()

   def pan_ended(self,pan):
      '''called when scaling is complete'''
      self.motion_ended()
      
   def convert_point(self,point_px, stop=False):
      '''
      given a touch point in the view space, compute the corresponding point in data coords. assumes linear scaling!
      TODO: support log scaling 
      
      there are basically two bbox transforms:  1) from figure coords to view coords, accounting for sign change in y. this then lets us compute axes box in view coords, and generate 2) transform from view to data coords.

      '''
      transFig=BboxTransformTo(Bbox([(0,self.height),(self.width,0)]))
      bbox_axes=Bbox(transFig.transform(plt.gca().get_position()))
      bbox_data=Bbox([(self.xlim[0],self.ylim[0]),(self.xlim[1],self.ylim[1])])
      transMPL=BboxTransform(bbox_axes,bbox_data)
      self.trans=transMPL
      ax_pt=transMPL.transform_point(point_px)      
      return ax_pt
      
   def compute_lims(self):
      '''compute new axes limits based on pan/zoom.
         we want the opzoom centered on the scale centroid, so:
      
      new axes= (axes-ax_zoomctr)*scale + dp*scale + ax_zoomctr

      where each of these are converted to data units as needed.
      '''

      zoomctr=np.array([self.convert_point(self.centroid)]).T
      ax=[self.xlim,self.ylim]
      scale=[[1/self.sx],[1/self.sy]]
      dp=-np.matrix(self.trans.get_matrix()[0:2,0:2])*[[self.panx],[self.pany]]
      new_axes=np.array((ax-zoomctr)*scale+ np.array(dp)*np.array(scale)+zoomctr)
      return new_axes[0],np.sort(new_axes[1])

   def motion_ended(self):
      '''called when motion ends.  clean up scale/pan parms, and render final version'''
      logger.debug('motion end')
      lims=self.compute_lims()
      # set limits to mpl
      self.xlim=lims[0]
      self.ylim=lims[1]      
      # clean up
      self.sx,self.sy=1,1
      self.panx,self.pany=0,0
      #render
      self.update_plt(dpi=self.high_dpi,waitForLock=True)

   def update_transform(self):
      '''if lock can be acquired, start rendering thread, otherwise return.
      TODO:  while rendering, just update .transform.  update_plt would need to reset .transform'''
      
      if self.ready.acquire(False):
         self.update_plt(dpi=self.low_dpi)

if __name__=='__main__':
   v=ui.View(frame=(0,0,700,700))
   if 0:
      p=PinchView(frame=(0,0,400,400))
      im=ui.ImageView(frame=(0,0,400,400))
      im.image=ui.Image.named('test:Sailboat')
      p.add_subview(im)
      v.add_subview(p)
      p.add_subview(im)
   else:
      x=np.linspace(0,51,3501)
      plt.plot(np.sin(x)*np.exp(-x/5)+np.cos(5*x)*(1-np.exp(-x/2)),marker='o')
      m=MPLView(frame=v.bounds,flex='wh')
      v.add_subview(m)

   v.present('sheet')