from __future__ import print_function
# https://forum.omz-software.com/topic/2230/selectors-in-python/9

# coding: utf-8

import os
frameworks=os.listdir('/System/Library/Frameworks')
for f in frameworks:
    print(f)

# to load a Framework
from objc_util import *
ObjCClass('NSBundle').bundleWithPath_('/System/Library/Frameworks/FRAMEWORK_TO_LOAD.framework').load()