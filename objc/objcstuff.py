# coding: utf-8

# https://github.com/jsbain/objc_hacks/blob/master/objcstuff.py

import objc_util,ui

v=ui.View()

vv=objc_util.ObjCInstance(v._objc_ptr)

wnd= objc_util.ObjCClass('UIWindow').alloc()
r=objc_util.CGRect(objc_util.CGPoint(0,0),objc_util.CGSize(100,100))

wnd.initWithFrame_(r)