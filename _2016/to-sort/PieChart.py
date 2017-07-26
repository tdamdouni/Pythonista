# coding: utf-8

# https://forum.omz-software.com/topic/2919/making-arcs-and-filling-them-with-in-ui-path/5

# Below is a little example that draws a simple pie chart of the sort that's sometimes used for progress indicators. You simply pass the progress (between 0.0 and 1.0) to the draw_pie() function, and it'll return an image with a filled pie segment.

# It would be pretty easy to use similar code in the draw method of a custom view instead of creating an image. Hope this helps.

import ui
from math import pi, sin, cos, radians

def draw_pie(p, r, fill_color='black'):
	p = max(0.0, min(1.0, p))
	with ui.ImageContext(r * 2, r * 2) as ctx:
		ui.set_color(fill_color)
		path = ui.Path()
		center = ui.Point(r, r)
		path.move_to(center.x, center.y)
		start = radians(-90)
		end = start + p * radians(360)
		path.add_arc(r, r, r, start, end)
		path.close()
		ui.set_color(fill_color)
		path.fill()
		return ctx.get_image()
		
pie_img = draw_pie(0.75, 200)
pie_img.show()

