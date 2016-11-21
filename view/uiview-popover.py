# https://forum.omz-software.com/topic/3318/exception-when-opening-ui-view-using-popover-style

import ui
from scene import *

class MyScene(Scene):
	def setup(self):
		self.menu = ui.View(frame=(0, 0, 200, 200))
		
	def touch_began(self, touch):
		self.menu.present('popover', popover_location=touch.location)
		
		
run(MyScene())

