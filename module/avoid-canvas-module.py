# https://forum.omz-software.com/topic/3284/what-s-with-canvas-in-pythonista-3/13

# @omz

# ui.ImageContext

import ui

with ui.ImageContext(512, 512) as ctx:
	circle = ui.Path.oval(100, 100, 200, 200)
	ui.set_color('red')
	circle.fill()
	img = ctx.get_image()
	img.show()

