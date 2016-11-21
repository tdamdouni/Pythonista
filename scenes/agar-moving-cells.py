from scene import *
from random import *

class Particle(object):
	def __init__(self, wh):
		self.w = wh.w
		self.h = wh.h
		self.x = randint(0, self.w)
		self.y = randint(0, self.h)
		self.vx = 0
		self.vy = 0
		self.colour = Color(random(), random(), random())
		
	def update(self):
		self.x += self.vx
		self.y += self.vy
		if self.x > self.w:
			self.x = self.w
			self.vx *= -1
		if self.x < 0:
			self.x = 0
			self.vx *= -1
		if self.y > self.h:
			self.y = self.h
			self.vy *= -1
		if self.y < 0:
			self.y = 0
			self.vy *= -1
			
	def draw(self):
		fill(*self.colour)
		rect(self.x, self.y, 8, 8)
		
class Intro(Scene):
	def setup(self):
		self.particles = []
		for p in xrange(100):
			self.particles.append(Particle(self.size))
			
	def draw(self):
		background(0.00, 0.05, 0.20)
		for p in self.particles:
			p.update()
			p.draw()
			
	def touch_began(self, touch):
		global x1
		global y1
		x1=touch.location.x
		y1=touch.location.y
		
		
	def touch_moved(self, touch):
		x=touch.location.x
		y=touch.location.y
		
		for p in self.particles:
			if x1 > x:
				p.vx = 1
			if x1 < x:
				p.vx = -1
			if y1 > y:
				p.vy = 1
			if y1 < y:
				p.vy = -1
			if x1 == x:
				p.vx = 0
			if y1 == y:
				p.vy = 0
				
	def touch_ended(self, touch):
		for p in self.particles:
			p.vx = 0
			p.vy = 0
			
run(Intro())

