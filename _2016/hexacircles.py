# https://github.com/zacbir/pythonista

import canvas
import random
import math

from devices import *
from kuler import *

random.seed()

width, height = cinema
circle_size = 256.0
step = math.sqrt(circle_size**2 - (circle_size / 2.0)**2)

palette = random.choice(themes)

canvas.begin_updates()

canvas.set_size(width, height)
canvas.set_fill_color(*palette.darkest)
canvas.fill_rect(0, 0, width, height)

for x in range(100):
	r, g, b = random.choice(palette.colors)
	a = random.random() * 0.5 + 0.25
	canvas.set_fill_color(r, g, b, a)
	origin_x = random.random() * width
	origin_y = random.random() * height
	csize = random.random() * (width / 8.0) + (width / 16.0)
	canvas.fill_ellipse(origin_x, origin_y, csize, csize)

def rstrokedline(start_x, start_y, end_x, end_y):
	line_width = random.random() * 0.25 + 0.25
	canvas.set_line_width(line_width)
	r, g, b = palette.lightest
	a = random.random() * 0.25 + 0.05
	canvas.set_stroke_color(r, g, b, a)
	canvas.draw_line(start_x, start_y, end_x, end_y)

def hexacircle(start_x, start_y):
	r, g, b = random.choice(palette.colors)

	canvas.set_fill_color(r, g, b, random.random() * 0.75 + 0.25)
	s_r, s_g, s_b = palette.lightest
	canvas.set_stroke_color(s_r, s_g, s_b, random.random() * 0.50 + 0.50)
	canvas.set_line_width(random.random() * 0.25 + 0.25)
	circle = (start_x - (0.5 * circle_size),
	          start_y - (0.5 * circle_size),
	          circle_size, circle_size)
	canvas.draw_ellipse(*circle)
	canvas.fill_ellipse(*circle)

	# draw lines
	rstrokedline(start_x, start_y - circle_size, start_x, start_y + circle_size)
	rstrokedline(start_x - step, start_y, start_x + step, start_y)

	rstrokedline(start_x - step, start_y - (0.5 * circle_size), start_x + step, start_y + (0.5 * circle_size))
	rstrokedline(start_x - step, start_y + (0.5 * circle_size), start_x + step, start_y - (0.5 * circle_size))

	rstrokedline(start_x - step, start_y + (1.5 * circle_size), start_x + step, start_y - (1.5 * circle_size))
	rstrokedline(start_x - step, start_y - (1.5 * circle_size), start_x + step, start_y + (1.5 * circle_size))
    
	rstrokedline(start_x - step, start_y + (2.5 * circle_size), start_x + step, start_y - (2.5 * circle_size))
	rstrokedline(start_x - step, start_y - (2.5 * circle_size), start_x + step, start_y + (2.5 * circle_size))
    
	rstrokedline(start_x - (3.0 * step), start_y + (0.5 * circle_size), start_x + (3.0 * step), start_y - (0.5 * circle_size))
	rstrokedline(start_x - (3.0 * step), start_y - (0.5 * circle_size), start_x + (3.0 * step), start_y + (0.5 * circle_size))

for x in xrange(int(math.ceil(width/circle_size))+1):
	for y in xrange(int(math.ceil(height/circle_size))+1):
		center_x = x * (2.0 * step)
		center_y = y * circle_size
		hexacircle(center_x, center_y)
		hexacircle(center_x + step, center_y + (0.5 * circle_size))

canvas.end_updates()
