# https://forum.omz-software.com/topic/3318/exception-when-opening-ui-view-using-popover-style/3

import ui
from scene import *
class MyScene(Scene):
	def setup(self):
		self.menu = ui.View(frame=(0, 0, 200, 200))
		self.menu.name = 'popup'
	def touch_began(self, touch):
		self.menu.present('popover',popover_location=touch.location)
		ui.delay(self.popup_close,2)
	def popup_close(self):
		self.menu.close()
run(MyScene())

