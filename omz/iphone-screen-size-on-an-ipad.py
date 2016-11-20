# coding: utf-8

# @omz

# https://forum.omz-software.com/topic/2167/iphone-screen-size-on-an-ipad/2

from objc_util import *

# NOTES: width/height values refer to portrait orientation -- they're automatically
# swapped if the app is in landscape mode. When this is run with the same values
# again, the default window size (full-screen) is restored.

# Some things don't work correctly with a non-default window size, e.g. the copy/paste
# menu is positioned incorrectly.

WIDTH = 375
HEIGHT = 667

UIWindow = ObjCClass('UIWindow')
UIApplication = ObjCClass('UIApplication')
UIScreen = ObjCClass('UIScreen')

@on_main_thread
def resize_main_window(w, h):
	app = UIApplication.sharedApplication()
	win = app.keyWindow()
	wb = win.bounds()
	sb = UIScreen.mainScreen().bounds()
	if sb.size.width > sb.size.height:
		w, h = h, w
	if w == wb.size.width and h == wb.size.height:
		w, h = sb.size.width, sb.size.height
		
	win.setBounds_(((0, 0), (w, h)))
	win.setClipsToBounds_(True)
	
if __name__ == '__main__':
	resize_main_window(WIDTH, HEIGHT)
	
# --------------------

