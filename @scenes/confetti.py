# https://gist.github.com/GuyCarver/4180724
# Modified Particles sample to show rotating rectangles.

import canvas
from scene import *
from random import random
from colorsys import hsv_to_rgb
from threading import Thread, Event

p_size = 64
mt = True 

def GetVel () :
	return random() * 240 - 120

def GetSize () :
	return random() * 24 + 8
	
def GetAngVel () :
	return random() * 600 - 300
	
def getrect() :
	w = GetSize()
	h = GetSize()
	return Rect(-w, -h, w * 2, h * 2)

class Particle (object):
	def __init__(self, location):
		self.velocity = Size(GetVel(), GetVel())
		self.angle = 0
		self.angvel = GetAngVel()
		self.r = getrect()
		self.location = location
		self.hue = random()
		self.alpha = 1.0
		self.scale = 1.0
		self.scalerate = random() * 0.5
		
	def updateangle( self, time )	:
		v = self.angle + self.angvel * time
		while v > 360 : v -= 360
		while v < 0 : v += 360
		self.angle = v
		
	def draw(self) :
		r, g, b = hsv_to_rgb(self.hue, 1, 1)
		a = self.alpha
		x, y = self.location.as_tuple()
		push_matrix()
		translate(x, y)
		rotate(self.angle)
		scale(self.scale)
		fill(r * a,g * a,b * a,a)
		rect(self.r.x, self.r.y, self.r.w, self.r.h)
		pop_matrix()
			
	def update(self, time):
		self.updateangle(time)
		self.alpha -= 0.6 * time
		self.scale -= self.scalerate * time
		#self.hue += 0.12 * time
		self.location.x += self.velocity.w * time
		self.location.y += self.velocity.h * time
		return self.alpha <= 0
				
class Particles (Scene):
	def setup(self):
		self.show_instructions = True
		self.particles = []
		self.dead = set()
		p_size = 64 if self.size.w > 700 else 32
		if mt:
			self.udstart = Event()
			self.uddone = Event()
			self.udthread = Thread(target=self.bgupdate)
			self.udthread.start()
	
	def should_rotate(self, orientation):
		return True
	
	def touch_began(self, touch):
		if self.show_instructions:
			self.show_instructions = False
			blend_mode(canvas.BLEND_DESTINATION_ATOP)
		self.touch_moved(touch)
	
	def touch_moved(self, touch):
		if self.dead :
			particle = self.dead.pop()
			particle.__init__(touch.location)
		else:
		  particle = Particle(touch.location)
		  self.particles.append(particle)

	def bgupdate(self):
		while True:
			self.udstart.wait() #Wait for main thread to signal update.
			self.udstart.clear() #Clear signal.
			l = len(self.particles)
			h = l / 2
			for i in xrange(h, l):
				p = self.particles[i]
				if p.update(self.dt):
					self.dead.add(p)
			self.uddone.set() #Signal update done.		

	def draw(self):
		background(0, 0, 0)
		if self.show_instructions:
			s = 40 if self.size.w > 700 else 17
			text('Move your fingers across the screen.',
			     'Futura', s, *self.bounds.center().as_tuple())

		domt = False
		if mt:
			self.udstart.set()
			h = len(self.particles) / 2
			if h > 10:
				domt = True
				for i in xrange(h):
					p = self.particles[i]
					if p.update(self.dt):
						self.dead.add(p)
				self.uddone.wait()
				self.uddone.clear()

		for particle in self.particles:
			if particle.alpha > 0:
				particle.draw()
				if not domt:
					if particle.update(self.dt):
						self.dead.add(particle)

		tmg = int((self.dt) * 1000.0)
		text(str(tmg), x=20, y=20, alignment=9)

run(Particles())