from random import *
from scene import *

class Velocity(object):
	def __init__(self, dx, dy):
		self.dx = dx
		self.dy = dy

class Circle(object):
	def __init__(self, location, color, velocity):
		self.location = location
		self.color = color
		self.velocity = velocity

class CircleMove(Scene):
	def __init__(self):
		self.circles = []
	
	def draw(self):
		background(0, 0, 0)
		for circle in self.circles:
			fill(circle.color.r, circle.color.g, circle.color.b)
			circle.location.x += circle.velocity.dx
			circle.location.y += circle.velocity.dy
			ellipse(circle.location.x - 50, circle.location.y - 50, 50, 50)

	def touch_began(self, touch):
		location = touch.location
		random_color = Color(random(), random(), random())
		max_speed = 20
		random_velocity = Velocity(randint(-max_speed, max_speed), randint(-max_speed, max_speed))
		circle = Circle(location, random_color, random_velocity)
		self.circles.append(circle)

run(CircleMove())
