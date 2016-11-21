# coding: utf-8

# https://forum.omz-software.com/topic/2632/help-with-screen-sizes/19

import ui, scene

scale = scene.get_screen_scale()
with ui.ImageContext(100, 100) as ctx:
	ui.set_color('white')
	ui.fill_rect(0, 0, 100, 100)
	ui.set_color('black')
	ui.fill_rect(0, 3, 100, 2)
	ui.set_color('black')
	ui.fill_rect(0, 7, 100, 1)
	if scale > 1:
		ui.set_color('black')
		ui.fill_rect(0, 10, 100, 1 / scale)
	img = ctx.get_image()
	img.show()

