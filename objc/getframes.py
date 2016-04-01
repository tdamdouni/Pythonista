# coding: utf-8

# https://github.com/jsbain/objc_hacks/blob/master/getframes.py

'''
get frames of a video, and show them in an imageview.
based on objc code below
AVURLAsset *asset = [[AVURLAsset alloc] initWithURL:url options:nil];
AVAssetImageGenerator *generator = [[AVAssetImageGenerator alloc] initWithAsset:asset];
generator.requestedTimeToleranceAfter =  kCMTimeZero;
generator.requestedTimeToleranceBefore =  kCMTimeZero;
for (Float64 i = 0; i < CMTimeGetSeconds(asset.duration) *  FPS ; i++){
  @autoreleasepool {
    CMTime time = CMTimeMake(i, FPS);
    NSError *err;
    CMTime actualTime;
    CGImageRef image = [generator copyCGImageAtTime:time actualTime:&actualTime error:&err];
    UIImage *generatedImage = [[UIImage alloc] initWithCGImage:image];
    [self saveImage: generatedImage atTime:actualTime]; // Saves the image on document directory and not memory
    CGImageRelease(image);
  }
}
'''

from objc_util import *
import ui,time
file=os.path.expanduser('~/Documents/capturedvideo.MOV')
if not os.path.exists(file):
   raise IOError
asset=ObjCClass('AVURLAsset').alloc().initWithURL_options_(nsurl(file),None)
generator=ObjCClass('AVAssetImageGenerator').alloc().initWithAsset_(asset)

from ctypes import c_int32,c_uint32, c_int64,byref,POINTER,c_void_p,pointer,addressof

CMTimeValue=c_int64
CMTimeScale=c_int32
CMTimeFlags=c_uint32
CMTimeEpoch=c_int64
class CMTime(Structure):
   _fields_=[('value',CMTimeValue),
   ('timescale',CMTimeScale),
   ('flags',CMTimeFlags),
   ('epoch',CMTimeEpoch)]
   def __init__(self,value=0,timescale=1,flags=0,epoch=0):
      self.value=value
      self.timescale=timescale
      self.flags=flags
      self.epoch=epoch
z=CMTime(0,24)

generator.setRequestedTimeToleranceAfter_(z,restype=None,argtypes=[CMTime])
generator.setRequestedTimeToleranceBefore_(z,restype=None,argtypes=[CMTime])

# set up a view to display
root=ui.View(frame=(0,0,576,576))
iv=ui.ImageView(frame=root.bounds)
lbl=ui.Label(frame=(0,0,100,200),flex='LT')
lbl.text='frame'
root.add_subview(iv)
root.add_subview(lbl)
root.present('sheet')

lastimage=None  # in case we need to be careful with references
tactual=CMTime(0,1) #return value
t=CMTime(0,1)  # timescale is the important bit
for i in range(0,10):
   t.value=i
   cgimage_obj=generator.copyCGImageAtTime_actualTime_error_(t,byref(tactual),None,restype=c_void_p,argtypes=[CMTime,POINTER(CMTime),POINTER(c_void_p)])

   image_obj=ObjCClass('UIImage').imageWithCGImage_(cgimage_obj)
  
   def setimage():
      ObjCInstance(iv).setImage_(image_obj)
      lbl.text=str(tactual.value/tactual.timescale)
   #delay calls on different thread.  for some reason on_main_thread didnt work
   ui.delay(setimage,0)

   lastimage=image_obj #make sure this doesnt get gc'd
   time.sleep(1.0)
   
   
   

  