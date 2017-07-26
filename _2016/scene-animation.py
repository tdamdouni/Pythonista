# https://forum.omz-software.com/topic/2185/image-from-scene

from scene import *
from math import sin, cos

def polar2cart(r,theta):
	x = r*cos(theta)
	y = r*sin(theta)
	return x, y
	
	
class Particle():
	def __init__(self, location):
		self.location = location
		self.alpha=1
		
class ParticleSwirl(Scene):
	def setup(self):
		self.particles = set()
		self.theta=0
		
	def draw(self):
		background(0,0,0)
		global Particle
		self.theta += 1
		
		if self.theta % 2 == 0:
			self.particles.add(Particle((0,self.theta)))
			
		dead = set()
		for particle in self.particles:
			a=particle.alpha
			r,g,b = a,255*a,255*a
			fill(r,g,b,a)
			r, t = tuple(particle.location)
			x, y = polar2cart(r, t)
			
			drawx, drawy = x+self.size.w/2, y+self.size.h/2
			ellipse(drawx, drawy, 15,15)
			
			particle.alpha -= 0.006
			particle.location = (r+2,t+0.01)
			
			if particle.alpha <= 0:
				dead.add(particle)
				
		self.particles -= dead
		
		
		
run(ParticleSwirl())

