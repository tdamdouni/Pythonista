# coding: utf-8

# Captured from: _https://forum.omz-software.com/topic/2508/mfi-game-controller-support_

from __future__ import print_function
from objc_util import *

GCController = ObjCClass('GCController')
controllers = GCController.controllers()
print(controllers)

###==============================

from objc_util import *

classes = ObjCClass.get_names()
print(classes)

###==============================

# coding: utf-8
from objc_util import *

NSBundle = ObjCClass('NSBundle')
gc_framework = NSBundle.bundleWithPath_('/System/Library/Frameworks/GameController.framework')
gc_framework.load()

GCController = ObjCClass('GCController')
controllers = GCController.controllers()
print(controllers)
