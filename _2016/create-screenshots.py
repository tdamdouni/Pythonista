# https://forum.omz-software.com/topic/1523/controlling-screenshots/2

# To use this, create a script with UI, add a button or something like that, and set its action to screenshot_action. The result will be shown in the console, from where you could save it to your photos etc. If you run this on an iPhone, you'll need to close the UI to see it. And yes, I know that this method is not documented... Sorry about that. It's probably not what the OP was asking about anyway, but could still be useful sometimes.

import ui

def screenshot_action(sender):
	v = sender.superview
	with ui.ImageContext(v.width, v.height) as c:
		v.draw_snapshot()
		c.get_image().show()
		
v = ui.load_view()
v.present('sheet')

