import random
import math

from canvas import *
from kuler import *
from devices import *

random.seed()

def calculate_control_point(radius):
    return (4 * radius * (math.sqrt(2) - 1)) / 3


def calculate_center_square(width, height):
	is_square = is_portrait = is_landscape = False
	is_square = width / height == 1
	if not is_square:
		is_portrait = width / height < 1
		if not is_portrait:
			is_landscape = True
	square_size = min(width, height) / 2.0
	if is_square:
		offset = (square_size / 2.0, square_size / 2.0)
	if is_portrait:
		offset = (square_size / 2.0, (height - square_size) / 2.0)
	if is_landscape:
		offset = ((width - square_size) / 2.0, square_size / 2.0)
	return offset[0], offset[1], square_size


def draw_circle(x, y, size):
	radius = size / 2.0
	offset = calculate_control_point(radius)

	point1 = (x + radius, y)
	point2 = (x + size, y + radius)
	point3 = (x + radius, y + size)
	point4 = (x, y + radius)
	
	main_color = theme.lightest
	main_width = random.random() * 4.5 + 0.5
	off_color = shade_of(theme.lightest)
	off_width = random.random() * 0.75 + 0.5
	
	off = int(random.random() * 4)
	
	segment_colors = [main_color, main_color, main_color, main_color]
	segment_widths = [main_width, main_width, main_width, main_width]
	
	segment_colors[off] = off_color
	segment_widths[off] = off_width
	
	# stroke the circle
	begin_path()
	move_to(*point1)
	set_line_width(segment_widths[0])
	set_stroke_color(*segment_colors[0])
	add_curve(point1[0] + offset, point1[1], point2[0], point2[1] - offset, *point2)
	draw_path()
	begin_path()
	move_to(*point2)
	set_line_width(segment_widths[1])
	set_stroke_color(*segment_colors[1])
	add_curve(point2[0], point2[1] + offset, point3[0] + offset, point3[1], *point3)
	draw_path()
	begin_path()
	move_to(*point3)
	set_line_width(segment_widths[2])
	set_stroke_color(*segment_colors[2])
	add_curve(point3[0] - offset, point3[1], point4[0], point4[1] + offset, *point4)
	draw_path()
	begin_path()
	move_to(*point4)
	set_line_width(segment_widths[3])
	set_stroke_color(*segment_colors[3])
	add_curve(point4[0], point4[1] - offset, point1[0] - offset, point1[1], *point1)
	draw_path()


width, height = ipad_r
grid_x, grid_y, size = calculate_center_square(width, height)

theme = random.choice(themes)

set_size(width, height)

begin_updates()
set_fill_color(*theme.darkest)
fill_rect(0.0, 0.0, width, height)
number_of_circles = 25
for x in xrange(number_of_circles):
	step = size / (number_of_circles * 1.0)
	step += random.random() * step
	draw_circle(grid_x, grid_y, size)
	grid_x += step * 0.20
	grid_y += step * 0.80
	size -= step * 2
end_updates()

