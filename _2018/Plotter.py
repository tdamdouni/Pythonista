# Function Plotter

import canvas
import console
from math import sin, cos, pi

def draw_grid(min_x, max_x, min_y, max_y):
	w, h = canvas.get_size()
	scale_x = w / (max_x - min_x)
	scale_y = h / (max_y - min_y)
	min_x, max_x = round(min_x), round(max_x)
	min_y, max_y = round(min_y), round(max_y)
	canvas.begin_updates()
	canvas.set_line_width(1)
	canvas.set_stroke_color(0.7, 0.7, 0.7)
	#Draw vertical grid lines:
	x = min_x
	while x <= max_x:
		if x != 0:
			draw_x = round(w / 2 + x * scale_x) + 0.5
			canvas.draw_line(draw_x, 0, draw_x, h)
		x += 0.5
	#Draw horizontal grid lines:
	y = min_y
	while y <= max_y:
		if y != 0:
			draw_y = round(h/2 + y * scale_y) + 0.5
			canvas.draw_line(0, draw_y, w, draw_y)
		y += 0.5
	#Draw x and y axis:
	canvas.set_stroke_color(0, 0, 0)
	canvas.draw_line(0, h/2, w, h/2)
	canvas.draw_line(w/2, 0, w/2, h)
	canvas.end_updates()

def plot_function(func, color, min_x, max_x, min_y, max_y):
	#Calculate scale, set line width and color:
	w, h = canvas.get_size()
	origin_x, origin_y = w * 0.5, h * 0.5
	scale_x = w / (max_x - min_x)
	scale_y = h / (max_y - min_y)
	canvas.set_stroke_color(*color)
	canvas.set_line_width(2)
	canvas.move_to(origin_x + scale_x * min_x, 
	               origin_y + func(min_x) * scale_y)
	#Draw the graph line:
	x = min_x
	while x <= max_x:
		x += 0.05
		draw_x = origin_x + scale_x * x
		draw_y = origin_y + func(x) * scale_y
		canvas.add_line(draw_x, draw_y)
	canvas.set_fill_color(*color)
	canvas.draw_path()

#Set up the canvas size and clear any text output:
console.clear()
canvas.set_size(688, 688)
#Draw the grid:
area = (-pi, pi, -pi, pi)
draw_grid(*area)
#Draw 4 different graphs (sin(x), cos(x), x^2, x^3):
plot_function(sin, (1, 0, 0), *area)
plot_function(cos, (0, 0, 1), *area)
plot_function(lambda x: x ** 2, (0, 1, 1), *area)
plot_function(lambda x: x ** 3, (1.0, 0.5, 0), *area)
