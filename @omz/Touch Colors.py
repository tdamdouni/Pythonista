# https://gist.github.com/omz/5057356

# Variation of the 'Basic Scene' template that shows every
# touch in a different (random) color that stays the same
# for the duration of the touch.

from scene import *
from colorsys import hsv_to_rgb
from random import random

class TouchColors (Scene):
	def setup(self):
		self.touch_colors = {}
	
	def draw(self):
		background(0, 0, 0)
		for touch in self.touches.values():
			r, g, b = self.touch_colors[touch.touch_id]
			fill(r, g, b)
			ellipse(touch.location.x - 50, touch.location.y - 50, 100, 100)
	
	def touch_began(self, touch):
		self.touch_colors[touch.touch_id] = hsv_to_rgb(random(), 1, 1)
	
	def touch_moved(self, touch):
		pass

	def touch_ended(self, touch):
		del self.touch_colors[touch.touch_id]

run(TouchColors())