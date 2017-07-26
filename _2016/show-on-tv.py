# https://pythonista-app.slack.com/archives/projects/p1483739812000360

import ctypes
import objc_util
import ui

UIScreen = objc_util.ObjCClass("UIScreen")
UIView = objc_util.ObjCClass("UIView")
UIViewController = objc_util.ObjCClass("UIViewController")
UIWindow = objc_util.ObjCClass("UIWindow")

tvwin = None

def show_tv_view(v):
	global tvwin
	
	if UIScreen.screens().count() < 2:
		raise ValueError("No external screen connected")
	
	hide_tv_view()
	
	tv = UIScreen.screens()[1]
	tvwin = UIWindow.alloc().initWithFrame_(tv.bounds())
	tvwin.setScreen_(tv)
	
	vc = UIViewController.alloc().init()
	vc.setView_(objc_util.ObjCInstance(v))
	tvwin.setRootViewController_(vc)
	
	tvwin.setHidden_(False)

def hide_tv_view():
	if tvwin is not None:
		tvwin.setHidden_(True)

