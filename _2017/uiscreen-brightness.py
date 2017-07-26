https://forum.omz-software.com/topic/4182/ambient-light-sensor

from objc_util import *
screen = ObjCClass('UIScreen')
print(screen.mainScreen().brightness())
