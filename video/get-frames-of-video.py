# coding: utf-8

# https://forum.omz-software.com/topic/3621/video-edition/13

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

modified by jmv38
see discussion https://forum.omz-software.com/topic/3621/video-edition/1
'''
from objc_util import *
import ui,time,os,photos,gc
from math import ceil

# select a video
assets = photos.get_assets(media_type='video')
asset = photos.pick_asset(assets)
duration=asset.duration

# init frame picker
phasset=ObjCInstance(asset)
asseturl=ObjCClass('AVURLAsset').alloc().initWithURL_options_(phasset.ALAssetURL(),None)
generator=ObjCClass('AVAssetImageGenerator').alloc().initWithAsset_(asseturl)

from ctypes import c_int32,c_uint32, c_int64,byref,POINTER,c_void_p,pointer,addressof, c_double

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
c.CMTimeGetSeconds.argtypes=[CMTime]
c.CMTimeGetSeconds.restype=c_double

kCMTimeZero = CMTime.in_dll(c,'kCMTimeZero')
generator.setRequestedTimeToleranceAfter_(kCMTimeZero, restype=None, argtypes=[CMTime])
generator.setRequestedTimeToleranceBefore_(kCMTimeZero, restype=None, argtypes=[CMTime])

lastimage=None  # in case we need to be careful with references
fps = 30
tactual=CMTime(0,fps) #return value
currentFrame = 0
maxFrame = ceil(duration*fps)

def getFrame(i):
	t=CMTime(i,fps)
	cgimage_obj=generator.copyCGImageAtTime_actualTime_error_(t,byref(tactual),None,restype=c_void_p,argtypes=[CMTime,POINTER(CMTime),POINTER(c_void_p)])
	
	image_obj=ObjCClass('UIImage').imageWithCGImage_(cgimage_obj)
	ObjCInstance(iv).setImage_(image_obj)
	global lastimage
	lastimage=image_obj #make sure this doesnt get gc'd
	gc.collect() # to avoid pytonista random exit sometimes
	root.name=' frame:'+str(i)+' time:' +str(tactual.value/tactual.timescale)
	
# set up a view to display
root=ui.View(frame=(0,0,576,576))
iv=ui.ImageView(frame=(0,0,576,500))
root.add_subview(iv)

# a slider for coarse selection
sld = ui.Slider(frame=(100,500,376,76))
sld.continuous = False
root.add_subview(sld)
def sldAction(self):
	global currentFrame
	currentFrame = int(duration*self.value*fps)
	getFrame(currentFrame)
sld.action = sldAction

# buttons for frame by frame
prev = ui.Button(frame=(5,510,90,50))
prev.background_color = 'white'
prev.title = '<'
def prevAction(sender):
	global currentFrame
	currentFrame -= 1
	if currentFrame < 0: currentFrame = 0
	sld.value = currentFrame / fps / duration
	getFrame(currentFrame)
prev.action = prevAction
root.add_subview(prev)

nxt = ui.Button(frame=(480,510,90,50))
nxt.background_color = 'white'
nxt.title = '>'
def nxtAction(sender):
	global currentFrame
	currentFrame += 1
	if currentFrame > maxFrame: currentFrame = maxFrame
	sld.value = currentFrame / fps / duration
	getFrame(currentFrame)
nxt.action = nxtAction
root.add_subview(nxt)

root.present('sheet')
getFrame(currentFrame)

