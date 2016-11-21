# https://forum.omz-software.com/topic/3318/exception-when-opening-ui-view-using-popover-style/11

import ui
from scene import *

class MyScene(Scene):
	def setup(self):
		pass
		
	def get_viewpos_from_touch(self, touch):
		xt, yt = touch.location
		xw, yw = ui.get_window_size()
		return xt, yw - yt
		
	def touch_began(self, touch):
		menu = ui.View(frame=(0, 0, 200, 200))
		menu.present('popover', popover_location=self.get_viewpos_from_touch(touch))
		
		
run(MyScene())

