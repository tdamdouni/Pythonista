# coding: utf-8

# https://forum.omz-software.com/topic/2935/interacting-with-uitouches/2 

import ui
from objc_util import ObjCInstance

class MyView (ui.View):
	def touch_began(self, touch):
		ui_touch = ObjCInstance(touch)
		print(ui_touch)
		
MyView().present('sheet')

