# https://forum.omz-software.com/topic/2947/controlling-system-volume-objc_util/2

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

set_system_volume(0.5)
