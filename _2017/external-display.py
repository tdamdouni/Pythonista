# https://forum.omz-software.com/topic/4221/dual-screen-support/2

# create new script with UI, call it hdmi for example
# add some UI controls (I did add label with Hallo HDMI text)
# create another script with UI, call it main for example
# add some UI controls (I did add label with Hallo iPad text)

# Code for the hdmi.py:

import ui

def load_view():
	return ui.load_view()
	
# Code for the main.py:

import ui
import hdmi
import objc_util

v = ui.load_view()
v.present('sheet')

UIScreen = objc_util.ObjCClass('UIScreen')
if len(UIScreen.screens()) > 1:
	second_screen = UIScreen.screens()[1]
	
	bounds = second_screen.bounds()
	
	UIWindow = objc_util.ObjCClass('UIWindow')
	second_window = UIWindow.alloc().initWithFrame_(bounds)
	second_window.setScreen(second_screen)
	second_window.setHidden(False)
	
	hdmi_view = hdmi.load_view()
	hdmi_view_objc = objc_util.ObjCInstance(hdmi_view)
	hdmi_view_objc.setFrame(second_window.bounds())
	second_window.addSubview(hdmi_view_objc)

