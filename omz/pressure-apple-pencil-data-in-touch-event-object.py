# coding: utf-8

# @omz

# https://forum.omz-software.com/topic/3084/pressure-apple-pencil-data-in-touch-event-object

# It's relatively easy to convert a ui.Touch object to an Objective-C UITouch to get additional properties of the touch. Here's a very simple example (not tested with Apple Pencil, but I think it should behave the same as 3D Touch on an iPhone 6s)

import ui
from objc_util import ObjCInstance

class MyView (ui.View):
    def touch_moved(self, touch):
        ui_touch = ObjCInstance(touch)
        force = ui_touch.force()
        # To keep it simple, just show the force in the view's title bar:
        self.name = 'Force: %0.2f' % (force,)

v = MyView(frame=(0, 0, 320, 320))
v.present('sheet')
