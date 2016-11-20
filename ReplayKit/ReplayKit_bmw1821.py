# coding: utf-8 

# https://gist.github.com/bmw1821/de3ab9cb8bb4b7719571

# https://forum.omz-software.com/topic/2726/pythonista-replaykit

from objc_util import *
from Foundation import NSBundle

NSBundle.bundleWithPath_('/System/Library/Frameworks/ReplayKit.framework').load()
RPScreenRecorder = ObjCClass('RPScreenRecorder')

