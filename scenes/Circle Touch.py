# Copyright Matthew Murdoch
# Remix under the terms of the MIT license (see http://opensource.org/licenses/MIT)

from random import random
from scene import *

class Circle(object):
	def __init__(self, location, color):
		self.location = location
		self.color = color
		
class CircleTouch(Scene):
	def __init__(self):
		self.circles = []
		
	def draw(self):
		background(0, 0, 0)
		for circle in self.circles:
			fill(circle.color.r, circle.color.g, circle.color.b)
			ellipse(circle.location.x - 50, circle.location.y - 50, 50, 50)
			
	def touch_began(self, touch):
		location = touch.location
		random_color = Color(random(), random(), random())
		circle = Circle(location, random_color)
		self.circles.append(circle)
		
run(CircleTouch())

