# https://gist.github.com/jsbain/3e708b73a04e5fc2e04569d9556198e3

'''
minimal avplayer example
'''
from objc_util import *
AVPlayerItem=ObjCClass('AVPlayerItem')
AVPlayer=ObjCClass('AVPlayer')
AVPlayerLayer=ObjCClass('AVPlayerLayer')
import photos
def pick_asset():
	assets = photos.get_assets(media_type='video')
	asset = photos.pick_asset(assets)
	phasset=ObjCInstance(asset)
	asseturl=ObjCClass('AVURLAsset').alloc().initWithURL_options_(phasset.ALAssetURL(),None)
	return asseturl
#define cmtime, for seeking
import ctypes
CMTimeValue=ctypes.c_int64
CMTimeScale=ctypes.c_int32
CMTimeFlags=ctypes.c_uint32
CMTimeEpoch=ctypes.c_int64
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
c.CMTimeMakeWithSeconds.argtypes=[ctypes.c_double,ctypes.c_int32]
c.CMTimeMakeWithSeconds.restype=CMTime
c.CMTimeGetSeconds.argtypes=[CMTime]
c.CMTimeGetSeconds.restype=c_double
############_
u=pick_asset()
i=AVPlayerItem.playerItemWithAsset_(u)
p=AVPlayer.playerWithPlayerItem_(i)
videolayer=AVPlayerLayer.playerLayerWithPlayer_(p)

import ui
v=ui.View(frame=(0,0,500,500))
V=ObjCInstance(v)
videolayer.frame=V.bounds()
V.layer().addSublayer_(videolayer)
v.present('sheet')

duration=i.duration()
duration_sec=duration.a/duration.b
slider=ui.Slider(frame=(0,0,v.width,20))
@on_main_thread
def seek(t):
	T=c.CMTimeMakeWithSeconds(t,1)
	p.seekToTime_(T,argtypes=[CMTime],restype=None)
	
def slider_action(sender):
	seek(sender.value*duration_sec)
slider.action=slider_action
v.add_subview(slider)
p.play()
#exercise to reader:  implement p.pause()

