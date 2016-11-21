# http://stackoverflow.com/questions/32744730/why-isnt-my-scene-running-correctly

from scene import *
from random import *
class Particle(object):
	def __init__(self, wh):
		self.w = wh.w
		self.h = wh.h
		self.x = randint(0, self.w)
		self.y = randint(0, self.h)
		self.vx = randint(-10, 20)
		self.vy = randint(-10, 20)
		self.colour = Color(random(), random(), random())
		self.cells=Rect(self.x, self.y, 5, 5)
		cells=self.cells
		
	def update(self):
		self.x += self.vx
		self.y += self.vy
		self.vx *= 0
		self.vy *= 0
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
		ellipse(*self.cells)
		
class Intro(Scene):
	def setup(self):
		self.psize=13
		global plocx
		global plocy
		plocx=240
		plocy=160
		self.player = Rect(plocx, plocy, 20, 20)
		self.colour = Color(random(), random(), random())
		
		self.particles = []
		for p in range(100):
			self.particles.append(Particle(self.size))
			
	def touch_began(self, touch):
		global x1
		global y1
		x1=touch.location.x
		y1=touch.location.y
		
		
	def touch_moved(self, touch):
		global plocx
		global plocy
		global newplocx
		global newplocy
		x=touch.location.x
		y=touch.location.y
		if x > x1:
			addx=(x-x1)/4
			newplocx=plocx+addx
			
		if x < x1:
			subx=(x-x1)/4
			newplocx=plocx+subx
			
		if y > y1:
			addy=(y-y1)/4
			newplocy=plocy+addy
			
		if y < y1:
			suby=(y-y1)/4
			newplocy=plocy+suby
			
		xmin=215
		xmax=265
		ymin=140
		ymax=190
		
		while xmax > plocx and newplocx > plocx:
			plocx = plocx + 1
			self.player = Rect(plocx, plocy, 16, 16)
			
		while xmin < plocx and newplocx < plocx:
			plocx = plocx - 1
			self.player = Rect(plocx, plocy, 16, 16)
			
		while ymax > plocy and newplocy > plocy:
			plocy = plocy + 1
			self.player = Rect(plocx, plocy, 16, 16)
			
		while ymin < plocy and newplocy < plocy:
			plocy = plocy - 1
			self.player = Rect(plocx, plocy, 16, 16)
			
	def draw(self):
		background(0, 0.05, 0.2)
		self.player = Rect(plocx, plocy, self.psize, self.psize)
		for p in self.particles:
			p.update()
			p.draw()
			cells = p.cells
			if self.player.intersects(cells):
				self.newpsize=self.psize+0.2
				self.psize=self.newpsize
				self.particles.remove(p)
		ellipse(*self.player)
		
run(Intro(), LANDSCAPE)

