from __future__ import print_function
# https://gist.github.com/guyhillyer/4240849

# Mandelista: a Mandelbrot set explorer for Pythonista.
# Dragging selects a region which is highlighted;
# tapping inside the highlighted region zooms to the region;
# tapping outside the region cancels the selection.
# By Guy K Hillyer, a Python neophyte.
import sys
from scene import *

# The class Region represents the area of the graph that is being
# examined. It has two coordinate systems: the range of real numbers
# involved in the calcuations, and the corresponding range of pixels
# available on the display.  It also represents a zoom level which
# determines the relationship between the two coordinate systems.

class Region():

	# c_width: range of the real component of the complex number (float)
	# p_width: number of horizontal pixels on the output screen (int)
	# p_height: number of vertical pixels
	# center:  the Region is centered on this coordinate (complex)
	
	def __init__(self, center, c_width, p_width, p_height):
		self.c_center = center        # a complex number
		self.p_width = int(p_width)
		self.p_height = int(p_height)
		c_width = c_width * 1.0       # coerce it to be a float
		self.ppu = p_width / c_width  # pixels per c unit
		self.p_offset = (int(p_width/2 - self.c_center.real * self.ppu),
						 int(p_height/2 - self.c_center.imag * self.ppu))

	def translate_p_to_c(self, coord):
		x = (coord[0] - self.p_offset[0]) / self.ppu
		y = (coord[1] - self.p_offset[1]) / self.ppu
		return complex(x, y)

	def translate_c_to_p(self, c):
		x = c.real * self.ppu + self.p_offset[0]
		y = c.imag * self.ppu + self.p_offset[1]
		return (int(x), int(y))
	
	def is_portrait(self):
		return self.p_width <= self.p_height
	
	# Return a width that maintains the aspect ratio, with the given height
	def get_width_for(self, height):
		return int(1.0 * self.p_width / self.p_height * height)

	# Return a height that maintains the aspect ratio, with the given width
	def get_height_for(self, width):
		return int(1.0 * self.p_height / self.p_width * width)

# A Colors object maps an "escape velocity" to a color for display
# purposes.

class Colors():

	BACKGROUND_COLOR = (0.0, 0.5, 0.5)
	AXIS_COLOR = (0.0, 0.0, 0.5)
	SELECTION_STROKE_COLOR = (0.0, 0.0, 1.0)
	SELECTION_ANIMATION_COLOR = (0.0, 1.0, 0.0)
	COLORVALS = [.3, .5, .7]
	BLACK = (0.0, 0.0, 0.0)

	def __init__(self):
		# This color map was inspired by the work of Kenneth Moreland.
		# http://www.sandia.gov/~kmorel/documents/ColorMaps/
		self.colors = [
			(213,219,230),
			(204,217,238),
			(194,213,244),
			(184,208,249),
			(174,201,253),
			(163,194,255),
			(152,185,255),
			(141,176,254),
			(130,165,251),
			(119,154,247),
			(108,142,241),
			(119,154,247),
			(130,165,251),
			(141,176,254),
			(152,185,255),
			(163,194,255),
			(174,201,253),
			(184,208,249),
			(194,213,244),
			(204,217,238),
			(213,219,230),
			(229,216,209),
			(236,211,197),
			(241,204,185),
			(245,196,173),
			(247,187,160),
			(247,177,148),
			(247,166,135),
			(244,154,123),
			(241,141,111),
			(236,127,99),
			(229,112,88),
			(222,96,77),
			(229,112,88),
			(236,127,99),
			(241,141,111),
			(244,154,123),
			(247,166,135),
			(247,177,148),
			(247,187,160),
			(245,196,173),
			(241,204,185),
			(236,211,197),
			(229,216,209) ]

		# oops, we need floating point colors.
		for i in range(0, len(self.colors)):
			self.colors[i] = (self.colors[i][0]/255.0,
					  self.colors[i][1]/255.0,
					  self.colors[i][2]/255.0)
					  
# This constructor produces a different and gaudier color map.
#
#	def __init__(self):
#		self.colors = []
#		for a in Colors.COLORVALS:
#			for b in Colors.COLORVALS:
#				for c in Colors.COLORVALS:
#					self.colors.insert(0, (a,b,c))
					
	def get_color_for(self, v):
		if v == 0:
			# black is reserved for members of the set
			return Colors.BLACK

		return self.colors[v % len(self.colors)]

# VelocityGrid stores the calculated values for the current Region.
# It can supply already-calcuated values, to restore graph pixels that
# are temporarily obscured by other bits of UI.

class VelocityGrid():
	def __init__(self):
		self.clear()

	def put(self, x, y, val):
		self.grid[x, y] = val

	def get(self, x, y):
		try:
			return self.grid[x,y]
		except KeyError:
			return None

	def clear(self):
		self.grid = {}

# Mandelbrot is a subclass of Pythonista's Scene class.  The periodic
# invocation of draw() drives the calculation and display of the
# Mandelbrot Set.  The value of x is incremented by INCREMENT so that
# a general outline of the figure becomes visible quickly, as
# vertical lines separated by that many pixels are drawn.  Then
# subsequent passes fill in the lines that were previously skipped.

class Mandelbrot(Scene):
	
	DEFAULT_CENTER = complex(-.75, 0)
	INCREMENT = 10 # can be set to 1, to disable line-skipping

	def setup(self):
		# The initial region encompassess the whole Mandelbrot Set.
		if self.bounds.w < self.bounds.h:
			self.region = Region(Mandelbrot.DEFAULT_CENTER, 2.7,
			                     self.bounds.w, self.bounds.h)
		else:
			# calculate a width that will accommodate the set's
			# vertical extent, given the display's aspect ratio
			w = 1.0 * self.bounds.w / self.bounds.h * 2.4
			self.region = Region(Mandelbrot.DEFAULT_CENTER, w,
			                     self.bounds.w, self.bounds.h)

		# x represents the current c.real in z=z**2+c, in the
		# pixel coordinate system.  This value persists across
		# calls to the draw() method, which calculates and
		# displays for all visible y values on the current x
		# value.
		self.x = 0

		# To show the general shape of the result quickly, we skip x
		# values by INCREMENT, and fill in the gaps
		# on subsequent passes.  The number of passes is kept in passno.
		self.passno = 0

		# The Colors object decides which color to show for a given
		# "escape velocity."
		self.colors = Colors()

		self.root_layer = Layer(self.bounds)
		# add selection support data members
		self.init_selection()
		# set up to start calculating the current region
		self.init_graph()
		self.grid = VelocityGrid()
		self.sequence = breadth_first_binary_split(0, Mandelbrot.INCREMENT-1)
		self.x = self.sequence[0]

	def draw(self):
		if self.passno < Mandelbrot.INCREMENT:
			self.calc_one_line()
			self.x = self.x + Mandelbrot.INCREMENT
			if self.x >= self.region.p_width:
				self.passno = self.passno + 1
				if self.passno < Mandelbrot.INCREMENT:
					self.x = self.sequence[self.passno]

		self.root_layer.update(self.dt)
		self.root_layer.draw()

	# calc_one_line calculates and displays for all y values with
	# the current x value.  This results in one vertical line on
	# the display.  The display objects are Rectangles that are
	# 1 pixel wide.  To reduce the number of rectangles involved,
	# we combine adjacent pixels (on the y axis) that share the
	# same value into a single rectangle.  Very much like
	# run-length-encoding compression...
	def calc_one_line(self):
		saved_velocity = mandel(self.region.translate_p_to_c((self.x, 0)))
		self.grid.put(self.x, 0, saved_velocity)
		saved_y = 0
		length = 1

		for y in range(1, self.region.p_height):
			velocity = mandel(self.region.translate_p_to_c((self.x, y)))
			self.grid.put(self.x, y, saved_velocity)
			if velocity == saved_velocity:
				length = length + 1
			else:
				self.paint_line(self.x, saved_y, length, saved_velocity)
				saved_velocity = velocity
				saved_y = y
				length = 1

		self.paint_line(self.x, saved_y, length, saved_velocity)

	def paint_line(self, x, y, length, velocity):
		# If there is no velocity, then it has not been
		# calculated yet.  Paint the background color in this
		# case.
		if velocity == None:
			col = Colors.BACKGROUND_COLOR
		else:
			col = self.colors.get_color_for(velocity)
		fill(col[0], col[1], col[2])
		stroke_weight(0) # Workaround.  Why do I need this?
		rect(x, y, 1, length)

	# walk around the given rectangle, re-drawing the current
	# graph.  This replaces the selection-highlighting rectangle,
	# effectively removing it from the display. If weight is
	# greater than 1, then there is another rectangle immediately
	# nested inside the first rectangle, which is handled by the
	# recursion.

	def erase_rect(self, r, weight):

		if weight == 0:
			return

		ybottom = r.y
		ytop = r.y + r.h -1
		for x in range(int(r.x), int(r.x + r.w)):
			velocity = self.grid.get(x, ybottom)
			self.paint_line(x, ybottom, 1, velocity)
			velocity = self.grid.get(x, ytop)
			self.paint_line(x, ytop, 1, velocity)

		xleft = r.x
		xright = r.x + r.w - 1
		for y in range(int(r.y), int(r.y + r.h)):
			velocity = self.grid.get(xleft, y)
			self.paint_line(xleft, y, 1, velocity)
			velocity = self.grid.get(xright, y)
			self.paint_line(xright, y, 1, velocity)

		inner_rect = Rect(r.x + 1, r.y + 1, r.w - 2, r.h - 2)
		self.erase_rect(inner_rect, weight - 1)

	def init_graph(self):
		col = Colors.BACKGROUND_COLOR
		background(col[0], col[1], col[2])
		# show the axes on the graph, if they are visible.
		col = Colors.AXIS_COLOR
		fill(col[0], col[1], col[2])
		zero = self.region.translate_c_to_p(complex(0,0))
		rect(zero[0], 0, 1, self.region.p_height)
		rect(0, zero[1], self.region.p_width, 1)

	# Dragging creates a rectangular selection which is highlighted.
	# Tapping inside this rectangle zooms to the selected region.
	# Tapping outside this rectangle cancels the selection.

	def touch_began(self, touch):
		self.selection_origin = touch.location

	def touch_moved(self, touch):
		self.selected = False
		if not (self.selection.frame.w == 0 or self.selection.frame.h == 0):
			self.erase_rect(self.selection.frame, 2)
		x_vals = sorted((self.selection_origin.x, touch.location.x))
		y_vals = sorted((self.selection_origin.y, touch.location.y))
		ll_corner = Point(x_vals[0], y_vals[0])
		width = x_vals[1] - x_vals[0]
		height = y_vals[1] - y_vals[0]
		self.selection.frame = Rect(ll_corner.x, ll_corner.y, width, height)

	def touch_ended(self, touch):
		if self.selected:
			self.erase_rect(self.selection.frame, 2)
			if touch.location in self.selection.frame:
				self.zoom()
			self.selection.frame = Rect()
			self.selected = False
		else:
			self.selected = True

	def zoom(self):
		self.x = self.sequence[0]
		self.passno = 0
		f = self.selection.frame
		left = self.region.translate_p_to_c((f.x, f.y))
		right = self.region.translate_p_to_c((f.x + f.w, f.y + f.h))
		c_width = abs(right.real - left.real)
		center = self.region.translate_p_to_c((f.x + f.w/2, f.y + f.h/2))
		self.region = Region(center, c_width, self.bounds.w, self.bounds.h)
		self.init_graph()
		self.grid.clear()

	# This doesn't seem to work, in fact it is not called at all.
	def should_rotate(self, orientation):
		print('should_rotate called with', orientation)
		return False

	def init_selection(self):
		self.selected = False
		self.selection = Layer()
		self.add_layer(self.selection)
		self.selection.stroke_weight = 2
		col = Colors.SELECTION_STROKE_COLOR
		self.selection.stroke = Color(col[0], col[1], col[2])
		col = Colors.SELECTION_ANIMATION_COLOR
		self.selection.animate('stroke', Color(col[0], col[1], col[2]),
				       duration=.05, autoreverse=True,
				       repeat=sys.maxint)

# Perform the iterative Mandelbrot Set calculation z -> z ^ 2 + c.
# The value returned is either zero, which means that we consider
# c to be a member of the set; or a positive integer representing
# c's "escape velocity"

def mandel(c):
	
	# A shortcut for the biggest membership chunk: avoid the long
	# calculation for this large swath of contiguous values that
	# we know in advance to be members of the set.  This speeds
	# things up considerably when graphing the whole set.
	if c.real > -0.45 and c.real < 0.2 and c.imag > -0.5 and c.imag < 0.5:
		return 0

	z = complex(0,0)
	for i in range(1, 42):
		z = z**2 + c
		if abs(z) > 2:
			return i
	return 0
	
# Return an array that includes every integer from begin to end, in
# order such that each subsequent index splits the range, or a
# previously determined sub-range, in half (integerwise).  For
# example, given begin = 1 and end = 8, the sequence will be:
#     [4, 2, 6, 1, 3, 5, 7, 8]
# The first number is 4 because  it's halfway between 1 and 8.
# The second number is 2 because it's halfway between 1 and 4.
# The third number is 6 because it's halfway between 4 and 8.
# And so on.  This is used to determine the sequence of drawing vertical
# lines on the graph, so that each subsequently drawn line fills in the
# middle of the largest gap between previously drawn lines.
#
# The algorithm is interesting because it is very similar to one
# usually prescribed for breadth-first traversal of a binary tree.

def breadth_first_binary_split(begin, end):
	result = []
	
	q = []
	q.insert(0, (begin,end))
	
	while len(q) > 0:
		r = q.pop()
		mid = (r[0] + r[1]) / 2
		result.append(mid)
		if(r[0] < mid):
			q.insert(0, (r[0], mid - 1))
		if(r[1] > mid):
			q.insert(0, (mid + 1, r[1]))
			
	return result

scene = Mandelbrot()
run(scene)

