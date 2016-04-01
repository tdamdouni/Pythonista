import canvas
import random
import math

from devices import *
from kuler import *

random.seed()

width, height = ipad_r
palette = random.choice(themes)

canvas.begin_updates()

canvas.set_size(width, height)
canvas.set_fill_color(*palette.darkest)
canvas.fill_rect(0, 0, width, height)

square_size = 32.0

def fill_square(x, y, size, theme):
	canvas.set_fill_color(*shade_of(random.choice(theme.colors)))
	canvas.draw_rect(x, y, x + size, y + size)
	
def fill_triangles(x, y, size, theme):
	# fill upper triangle
	canvas.set_fill_color(*shade_of(random.choice(theme.colors)))
	canvas.begin_path()
	canvas.move_to(x, y)
	canvas.add_line(x, y + size)
	canvas.add_line(x + size, y + size)
	canvas.add_line(x, y)
	canvas.fill_path()
	
	# fill lower triangle
	canvas.set_fill_color(*shade_of(random.choice(theme.colors)))
	canvas.begin_path()
	canvas.move_to(x, y)
	canvas.add_line(x + size, y + size)
	canvas.add_line(x + size, y)
	canvas.add_line(x, y)
	canvas.fill_path()
	
for gx in xrange(int(width / square_size) + 1):
	for gy in xrange(int(height / square_size) + 1):
		#func = random.choice((fill_square, fill_triangles, fill_triangles, fill_triangles))
		fill_triangles(gx * square_size, gy * square_size, square_size, palette)

canvas.end_updates()
