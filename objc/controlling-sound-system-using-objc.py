# coding: utf-8

# @omz

# https://forum.omz-software.com/topic/2947/controlling-system-volume-objc_util

# There is no Apple-sanctioned way (public API) to do this, but this works on iOS 9.2 (things like this tend to break with system updates):

from objc_util import NSBundle, ObjCClass, on_main_thread
NSBundle.bundleWithPath_('/System/Library/Frameworks/MediaPlayer.framework').load()
MPVolumeView = ObjCClass('MPVolumeView')


@on_main_thread
def set_system_volume(value):
	volume_view = MPVolumeView.new().autorelease()
	for subview in volume_view.subviews():
		if subview.isKindOfClass_(ObjCClass('UISlider')):
			subview.value = value
			break
			
set_system_volume(0.8)

# There's probably a less convoluted way that I don't know of.

