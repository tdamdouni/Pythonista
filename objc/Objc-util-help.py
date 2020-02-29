# coding: utf-8

# https://forum.omz-software.com/topic/2958/need-help-with-objc_util

from __future__ import print_function
from objc_util import *
import ui
import time


# WORKS THE SAME WAY as in Myclass below
#cl = UIColor.alloc()
#cl = cl.init().initWithRed_green_blue_alpha_(.2, .3, .6, 1.).autorelease()


class Myclass (ui.View):
    def __init__(self):
        #ui.View.__init__(self) #changes nothing
        ocv = ObjCInstance(self._objc_ptr)
        cl = UIColor.blueColor()
        ocv.backgroundColor = cl

start = time.clock()
v = Myclass()
v.present('sheet')
print(time.clock()-start)

start = time.clock()
v2 = ui.View()
v2.background_color('blue')
v2.present('sheet')
print(time.clock()-start)
