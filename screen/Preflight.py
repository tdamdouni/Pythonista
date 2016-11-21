# coding: utf-8

# https://forum.omz-software.com/topic/2490/bounds-vrs-frame-center-etc-in-ui/19

import objc_util

def get_presented_size(mode,hide_title_bar=False):
	''' see https://forum.omz-software.com/topic/1618/any-ios-device/7'''
	f=objc_util.ObjCClass('UIApplication').sharedApplication().keyWindow().frame()
	sz= ui.Size(f.size.width,f.size.height)
	if sz[1]<=320:
		status_height=0
		title_height=32
	else:
		status_height=20
		title_height=44
		
	if mode=='sheet':
		maxsize=min( sz-(0,title_height*(not hide_title_bar)))
		return ui.Size(maxsize,maxsize)
	elif mode=='panel':
		return sz-(0,status_height+(title_height*(not hide_title_bar)))
	elif mode=='fullscreen':
		return sz-(0,(title_height*(not hide_title_bar)))

