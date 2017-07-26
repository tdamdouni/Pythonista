# https://forum.omz-software.com/topic/3774/toy-scene-script-drag-a-ball-around-with-elastic-string

# Ball.py by Ed Suominen
# Drag the ball around by an elastic string.
# Adapted from the AnalogClock example that comes with Pythonista
# Dedicated to the Public Domain

from scene import *
from math import hypot, atan2

RADIUS = 50
WIDTH = 4
SPEED = 0.04

class Ball(Scene):
	def setup(self):
		self.location = self.size/2
		circle = ui.Path.oval(0, 0, 2*RADIUS, 2*RADIUS)
		circle.line_width = 6
		shadow = ('black', 0, 0, 15)
		self.face = ShapeNode(circle, 'white', '#cccccc', shadow=shadow)
		self.add_child(self.face)
		self.vector = ShapeNode(
		ui.Path.rounded_rect(0, 0, 100, WIDTH, 3), 'red')
		self.vector.anchor_point = (0, 0.5)
		self.face.add_child(self.vector)
		self.face.add_child(
		ShapeNode(ui.Path.oval(0, 0, 2*WIDTH, 2*WIDTH), 'red'))
		self.did_change_size()
		
	def touch_began(self, touch):
		self.location = touch.location
		
	def touch_moved(self, touch):
		self.location = touch.location
		
	def update(self):
		d = self.location - self.face.position
		xy = self.face.position + SPEED * d
		self.face.position = xy
		length = hypot(*d)
		if length == 0:
			w = 0
		else:
			self.vector.rotation = atan2(d[1]/length, d[0]/length)
			if length < RADIUS:
				w = 2*WIDTH
			else:
				w = 2*WIDTH * RADIUS / length
		self.vector.size = (0.93*length, w)
		
	def did_change_size(self):
		self.face.position = self.size/2
		
scene = Ball()
run(scene)
