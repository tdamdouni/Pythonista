# https://github.com/zacbir/pythonista

try:
	from canvas import *
except ImportError:
	# We're in NodeBox
	def begin_updates():
		pass
		
	def end_updates():
		pass
		
	set_fill_color = fill
	fill_rect = rect
	fill_ellipse = oval
	set_stroke_color = stroke
	set_line_width = strokewidth
	move_to = moveto
	
	
	def draw_rect(x, y, width, height):
		"""capture and reset current fill color"""
		clr = fill()
		nofill()
		rect(x, y, width, height)
		fill(clr)
		
	def draw_ellipse(x, y, size_x, size_y):
		"""capture and reset current fill color"""
		clr = fill()
		nofill()
		oval(x, y, size_x, size_y)
		fill(clr)
		
	set_size = size

