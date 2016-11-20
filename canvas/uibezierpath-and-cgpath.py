# https://forum.omz-software.com/topic/3320/problem-with-uibezierpath-and-cgpath

import ui
from objc_util import *

a = ui.Path()
a.line_to(10, 0)
a.line_to(10, 10)
a.close()

b = ObjCInstance(a)
print(b.CGPath())

from objc_util import *
print(UIBezierPath.new().CGPath())

