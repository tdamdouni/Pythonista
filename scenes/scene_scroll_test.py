from scene import *
from math import exp
from threading import Thread
import datetime

# example scrolling scene with inertial scrolling
# basic scrolling example was by Dalorbi on the forums at:
#    http://omz-software.com/pythonista/forums/discussion/213/scrolling-in-scene-module/p1
# inertial scrolling added on by hroe

class MyScene (Scene):
	def setup(self):
		self.dx = self.size.w / 2
		self.dy = self.size.h / 2 + 10
		self.xy_velocity = None
		self.velocity_decay_timescale_seconds = 0.4
		self.max_retained_touch_points = 6
		self.min_velocity_points_per_second = 50
		self.cur_touch = None
		
	def draw(self):
		if self.xy_velocity is not None and self.cur_touch is None:
			self.dx += self.xy_velocity[0] * self.dt
			self.dy += self.xy_velocity[1] * self.dt
			decay = exp( - self.dt / self.velocity_decay_timescale_seconds )
			self.xy_velocity = (self.xy_velocity[0] * decay, self.xy_velocity[1] * decay)
			if ((abs(self.xy_velocity[0]) <= self.min_velocity_points_per_second) and
			(abs(self.xy_velocity[1]) <= self.min_velocity_points_per_second)):
				self.xy_velocity = None
		background(0, 0, 0)
		translate(self.dx, self.dy)
		fill(1, 1, 1)
		stroke(1, 1, 1)
		stroke_weight(3)
		
		for x in range(-3000,3100,100):
			line(x,-3000,x,3000)
			text(str(x), font_size = 30, x = x, y = 0, alignment = 5)
			
		for y in range(-3000,3100,100):
			line(-3000,y,3000,y)
			text(str(y), font_size = 30, x = 0, y = y, alignment = 5)
			
		for i in range(-3000,3000,100):
			image('PC_Grass_Block',i,-125)
			
	def touch_began(self, touch):
		if self.cur_touch is None:
			self.cur_touch = touch.touch_id
			self.xy_velocity = None
			self.touch_log = []
			
	def touch_moved(self, touch):
		if touch.touch_id == self.cur_touch:
			self.dx += touch.location.x - touch.prev_location.x
			self.dy += touch.location.y - touch.prev_location.y
			self.touch_log.append((datetime.datetime.utcnow(), touch.location))
			self.touch_log = self.touch_log[-self.max_retained_touch_points:]
			
	def touch_ended(self, touch):
		if touch.touch_id == self.cur_touch:
			self.xy_velocity = None
			if len(self.touch_log) >= 2:
				dt = (self.touch_log[-1][0] - self.touch_log[0][0]).total_seconds()
				if dt > 0:
					x_velocity = (self.touch_log[-1][1].x - self.touch_log[0][1].x) / dt
					y_velocity = (self.touch_log[-1][1].y - self.touch_log[0][1].y) / dt
					self.xy_velocity = (x_velocity, y_velocity)
			self.cur_touch = None
			
run(MyScene())

