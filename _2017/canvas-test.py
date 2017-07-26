# coding: utf-8

# https://forum.omz-software.com/topic/3284/what-s-with-canvas-in-pythonista-3/24

import canvas
import colorsys
from six.moves import range

#this crashes Pythonista 2 and 3. canvas depracated?

w=h=512
canvas.set_size(w,h)

canvas.begin_updates()

def plot():
	canvas.clear()
	for x in range(1,512,2):
		for y in range(1,512,2):
			canvas.set_fill_color(.75,.25,.25)
			canvas.fill_ellipse(x,y,1,1)

plot()
canvas.end_updates()
