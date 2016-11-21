# https://forum.omz-software.com/topic/3368/objc-setstatusbarhidden-possible

from objc_util import *
import ui

#try to get a true full screen without any iOS status bar.

v = ui.View()
ObjCInstance(v).prefersStatusBarHidden_ = True #likely wrong but i'm not sure...
v.present(hide_title_bar=True)

shared_application = ObjCClass('UIApplication').sharedApplication()
shared_application.setStatusBarHidden_ = True

# --------------------

from objc_util import *
import ui

#try to get a true full screen without any iOS status bar.

v = ui.View()
ObjCInstance(v).prefersStatusBarHidden_ = True #likely wrong but i'm not sure...
v.present(hide_title_bar=True)

shared_application = ObjCClass('UIApplication').sharedApplication()
shared_application.setStatusBarHidden_ = True

