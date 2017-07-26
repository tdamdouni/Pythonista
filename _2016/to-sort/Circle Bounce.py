# Copyright Matthew Murdoch
# Remix under the terms of the MIT license (see http://opensource.org/licenses/MIT)
from random import *
from scene import *

class Rectangle(object):
	def __init__(self, bottom_left, size):
		self._rect = Rect(bottom_left.x, bottom_left.y, size.w, size.h)
		self._fill_color = Color(0, 0, 0)
	
	@property
	def center(self):
		return self._rect.center()

	@property
	def left(self):
		return self._rect.left()

	@property
	def right(self):
		return self._rect.right()

	@property
	def top(self):
		return self._rect.top()

	@property
	def bottom(self):
		return self._rect.bottom()

	@property
	def width(self):
		return self._rect.w

	@property
	def height(self):
		return self._rect.h

	@property
	def fill_color(self):
		return self._fill_color

	@fill_color.setter
	def fill_color(self, value):
		self._fill_color = value

	def __contains__(self, key):
		return key in self._rect

	def shrink(self, by):
		"""
		Shrinks the rectangle by an equal amount on each side.
		
		by: the amount by which to shrink each side
		"""
		return Rectangle(Point(self.left+by, self.bottom+by), 
		                 Size(self.width-2*by, self.height-2*by))

	def draw(self):
		fill(self.fill_color.r, self.fill_color.g, self.fill_color.b)
		rect(self.left, self.bottom, self.width, self.height)


class Velocity(object):
	def __init__(self, dx, dy):
		self.dx = dx
		self.dy = dy
		
	def bounce_off_vertical(self):
		self.dx = -self.dx
		
	def bounce_off_horizontal(self):
		self.dy = -self.dy


class Circle(object):
	def __init__(self, center, radius):
		self._center = center
		self._radius = radius
		self._fill_color = Color(0, 0, 0)
		self._velocity = Velocity(0, 0)
	
	@property
	def center(self):
		return self._center

	@property
	def radius(self):
		return self._radius
	
	@property
	def left(self):
		return self.center.x - self.radius

	@property
	def right(self):
		return self.center.x + self.radius

	@property
	def top(self):
		return self.center.y + self.radius

	@property
	def bottom(self):
		return self.center.y - self.radius

	@property
	def diameter(self):
		return 2 * self.radius
	
	@property
	def velocity(self):
		return self._velocity

	@velocity.setter
	def velocity(self, value):
		self._velocity = value
	
	@property
	def fill_color(self):
		return self._fill_color
		
	@fill_color.setter
	def fill_color(self, value):
		self._fill_color = value	
		
	def move(self, bounds):
		self.center.x += self.velocity.dx
		if self.left < bounds.left:
			self.center.x += bounds.left - self.left
			self.velocity.bounce_off_vertical()
		elif self.right > bounds.right:
			self.center.x -= self.right - bounds.right
			self.velocity.bounce_off_vertical()

		self.center.y += self.velocity.dy
		if self.bottom < bounds.bottom:
			self.center.y += bounds.bottom - self.bottom
			self.velocity.bounce_off_horizontal()
		elif self.top > bounds.top:
			self.center.y -= self.top - bounds.top
			self.velocity.bounce_off_horizontal()

	def draw(self):
		fill(self.fill_color.r, self.fill_color.g, self.fill_color.b)
		ellipse(self.left, self.bottom, self.diameter, self.diameter)


class CircleBounce(Scene):
	def __init__(self):
		self._circles = []
		self._box = None
	
	@property
	def box(self):
		if not self._box:
			screen = Rectangle(Point(0, 0), self.size)
			self._box = screen.shrink(100)
			self._box.fill_color = Color(0.5, 0.25, 0)
		
		return self._box
	
	def draw(self):
		self.box.draw()

		for circle in self._circles:
			circle.move(self.box)
			circle.draw()

	def touch_began(self, touch):
		if touch.location in self.box:
			center = touch.location
			radius = randrange(5, 50)
			circle = Circle(center, radius)
			max_speed = 15
			random_dx = randint(-max_speed, max_speed)
			random_dy = randint(-max_speed, max_speed)
			random_velocity = Velocity(random_dx, random_dy)
			random_color = Color(random(), random(), random())
			circle.fill_color = random_color
			circle.velocity = random_velocity
			self._circles.append(circle)

run(CircleBounce())
