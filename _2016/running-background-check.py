# https://forum.omz-software.com/topic/3799/testing-if-the-app-is-running-in-the-background

from objc_util import  *
from ctypes import *
import dialogs

def willResignActive_(_self,_sel,_notification):
   print('entering background')
   #do stuff here

    
MyBGDetector=create_objc_class('MyBGDetector',methods=[willResignActive_])
d=MyBGDetector.alloc().init()

UIApplicationWillResignActiveNotification=ObjCInstance(c_void_p.in_dll(c,'UIApplicationWillResignActiveNotification'))
NSNotificationCenter=ObjCClass('NSNotificationCenter')
NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(d, sel('willResignActive:'), UIApplicationWillResignActiveNotification, None)
