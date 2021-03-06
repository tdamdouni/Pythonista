# coding: utf-8

# https://forum.omz-software.com/topic/2632/help-with-screen-sizes/19

from __future__ import print_function
import ui
print(str(ui.get_screen_size()))

#==============================

import webbrowser
webbrowser.open('mactracker://ABA79B4E-3781-4053-8D73-AC46D16CE643')

#==============================

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

