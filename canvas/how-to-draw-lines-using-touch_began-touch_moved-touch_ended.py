# https://forum.omz-software.com/topic/3397/how-to-draw-lines-using-touch_began-touch_moved-touch_ended

import random, scene
from scene import *

class Particle(object):
	def __init__(self, wh):
		self.w = wh.w
		self.h = wh.h
		self.xblue = random.randint(0, self.w)
		self.yblue = random.randint(0, self.h)
		
		self.vxblue = 10
		self.vyblue = 10
		
		self.xred = random.randint(0, self.w)
		self.yred = random.randint(0, self.h)
		
		self.vxred = 10
		self.vyred = 10
		
		self.blueball = Rect(self.xblue, self.yblue, self.w/6, self.w/6)
		self.redball = Rect(self.xred, self.yred, self.w/6, self.w/6)
		
		
	def update(self):
		self.xblue += self.vxblue
		self.yblue += self.vyblue
		
		if self.xblue > self.w-100:
			self.xblue = self.w-100
			self.vxblue *= -1
		if self.xblue < 0:
			self.xblue = 0
			self.vxblue *= -1
		if self.yblue > self.h-100:
			self.yblue = self.h-100
			self.vyblue *= -1
		if self.yblue < 0:
			self.yblue = 0
			self.vyblue *= -1
			
			
			
		self.xred += self.vxred
		self.yred += self.vyred
		
		if self.xred > self.w-100:
			self.xred = self.w-100
			self.vxred *= -1
		if self.xred < 0:
			self.xred = 0
			self.vxred *= -1
		if self.yred > self.h-100:
			self.yred = self.h-100
			self.vyred *= -1
		if self.yred < 0:
			self.yred = 0
			self.vyred *= -1
			
			
		self.blueball = Rect(self.xblue, self.yblue, self.w/6, self.w/6)
		self.redball = Rect(self.xred, self.yred, self.w/6, self.w/6)
		
		
	def draw(self):
		fill('#3547ff')
		ellipse(*self.blueball)
		fill('#ff0b0b')
		ellipse(*self.redball)
		if self.blueball.intersects(self.redball):
			print('yay')
			
			
			
			
			
class MyScene(Scene):
	def setup(self):
		self.particles = []
		self.particles.append(Particle(self.size))
	def draw(self):
		background(0, 0, 0)
		for p in self.particles:
			p.update()
			p.draw()
			
			
run(MyScene(), PORTRAIT)
# --------------------

