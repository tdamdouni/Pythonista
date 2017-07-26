# https://forum.omz-software.com/topic/1523/controlling-screenshots/2

import ui

def screenshot_action(sender):
	v = sender.superview
	with ui.ImageContext(v.width, v.height) as c:
		v.draw_snapshot()
		c.get_image().show()
		
v = ui.load_view()
v.present('sheet')

