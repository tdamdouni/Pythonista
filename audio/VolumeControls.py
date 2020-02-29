# coding: utf-8

# https://gist.github.com/filippocld/c0deb6714a9aff9f1da9

from __future__ import print_function
from objc_util import NSBundle, ObjCClass, on_main_thread

NSBundle.bundleWithPath_('/System/Library/Frameworks/MediaPlayer.framework').load()
MPVolumeView = ObjCClass('MPVolumeView')
volume_view = MPVolumeView.new().autorelease()

@on_main_thread
def set_system_volume(value):
	volume_view.subviews()[0].value = value
	
@on_main_thread
def get_system_volume():
	return volume_view.subviews()[0].value()
	
	
def upAction():
	#Volume Up button has been pressed
	print('Up!')
	
def downAction():
	#Volume Down button has been pressed
	print('Down!')
	
	
default = get_system_volume()
def main():
	try:
		while True:
			if get_system_volume() > default:
				upAction()
				set_system_volume(default)
			elif get_system_volume() < default:
				downAction()
				set_system_volume(default)
	except KeyboardInterrupt:
		pass
		
if __name__ == '__main__':
	main()

