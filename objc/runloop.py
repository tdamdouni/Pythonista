# https://forum.omz-software.com/topic/3484/how-to-get-currentrunloop

from objc_util import *
NSRunLoop=ObjCClass('NSRunLoop')
r=NSRunLoop.currentRunLoop()

