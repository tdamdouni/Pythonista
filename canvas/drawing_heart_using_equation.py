#!python2
# coding: utf-8

# http://pastebin.com/ucWjRRfd

# draw a heart using equation
from __future__ import print_function
import canvas, sys, random
from console import clear
from datetime import datetime
from math import sin, cos, pi

w = h = 600 # canvas size
detail = random.random() * 100 # larger is slower
# almost perfect : 12.485 75.05 125.3
# half left : 12.525
# half right : 12.605
scale = 15 # larger is bigger
origin = w/2 # plot origin on canvas

def draw_heart(outline = False):
	first = True
	for t in xrange(int(2*pi * detail)):
		t = t * detail
		# heart equation
		x = 16*(sin(t) ** 3)
		y = 13*cos(t) - 5*cos(2*t) - 2*cos(3*t) - cos(4*t)
		# scale result
		x = origin + x * scale
		y = origin + y * scale + scale*2
		# hide first line
		if first:
			canvas.move_to(x, y)
			first = False
		else:
			canvas.add_line(x, y)
	# set color
	canvas.set_fill_color(1,0.5,0.5)
	canvas.set_stroke_color(0.5,0,0)
	canvas.set_line_width(detail/2)
	# draw heart
	if outline:
		canvas.draw_path()
	else:
		canvas.close_path()
		canvas.fill_path()
		
clear()
print('Calculating... d =',detail)
start = datetime.now()
canvas.set_size(w,h)
canvas.draw_rect(0,0, w,h)
#canvas.draw_line(0,h/2,w,h/2)
#canvas.draw_line(w/2,0,w/2,h)
draw_heart(True) # outlined
draw_heart() # filled
stop = datetime.now()
print(stop-start)

