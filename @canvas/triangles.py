import canvas
import random
import math

from devices import *
from kuler import *

random.seed()

width, height = iphone_5_ios7
triangle_side = 256.0
palette = random.choice(themes)

canvas.begin_updates()

canvas.set_size(width, height)
canvas.set_fill_color(*palette.darkest)
canvas.fill_rect(0, 0, width, height)

def draw_triangle(x, y, size, num_remaining):
	if num_remaining > 0:
		canvas.set_fill_color(*shade_of(random.choice(palette.colors)))
		canvas.set_stroke_color(*shade_of(random.choice(palette.colors)))
		canvas.set_line_width(random.random() * 0.5 + 0.5)
		step = math.sqrt(size**2 - (size / 2.0)**2)
		canvas.move_to(x - step, y - (size / 2.0))
		canvas.add_line(x, y + size)
		canvas.add_line(x + step, y - (size / 2.0))
		canvas.add_line(x - step, y - (size / 2.0))
		canvas.fill_path()
		canvas.draw_line(x - step, y - (size / 2.0), x, y + size)
		canvas.draw_line(x, y + size, x + step, y - (size / 2.0))
		canvas.draw_line(x + step, y - (size / 2.0), x - step, y - (size / 2.0))
		canvas.draw_line(x, y, x - (step / 2.0), y + (size / 4.0))
		canvas.draw_line(x, y, x + (step / 2.0), y + (size / 4.0))
		canvas.draw_line(x, y, x, y - (size / 2.0))
		canvas.draw_line(x - (step / 2.0), y + (size / 4.0), x + (step / 2.0), y + (size / 4.0))
		canvas.draw_line(x + (step / 2.0), y + (size / 4.0), x, y - (size / 2.0))
		canvas.draw_line(x, y - (size / 2.0), x - (step / 2.0), y + (size / 4.0))
		draw_triangle(random.random() * width, random.random() * height, random.random() * triangle_side, num_remaining - 1)

x = width / 2.0
y = height / 3.0 # figger
draw_triangle(x, y, triangle_side, 100)

canvas.end_updates()
