# coding: utf-8

# https://forum.omz-software.com/topic/140/crude-hittest

# https://gist.github.com/anonymous/68959f100b41187fa3d6

# Another example I have been playing with. In this one I modified the particles example because I wanted to test hitting a large array of objects. At about fifty it results in lag, probably because my coding is subpar

# Particles
#
# Create colorful bubbles by moving your fingers.

from scene import *
from random import random
from colorsys import hsv_to_rgb
grav=.1
inertia=.1

def hitCircles(x1,y1,size1,x2,y2,size2,output=0):
	radius1=float(size1/2) #radius
	radius2=float(size2/2)
	#need to find origins
	x1=float(x1)+size1/2
	y1=float(y1)+size1/2
	x2=float(x2)+size2/2
	y2=float(y2)+size2/2
 	#compare the distance to combined radii
 	dx = x2 - x1
	dy = y2 - y1
	radii = radius1 + radius2
	if((dx*dx)+(dy*dy)<radii*radii):
	#if size1+size2>=x2-x1+y2-y1:
		output=[dx,dy]
		#print str(dx)
	return output


class Particle (object):
	def __init__(self, location):
		self.velocity = Size(random() * 4 - 2, random() * 4 - 2)
		self.location = location
		self.hue = random()
		self.rebound=0.1
		self.alpha = 1.0

class Particles (Scene):
	def setup(self):
		self.show_instructions = True
		self.particles = set()
		self.p_size = 64 if self.size.w > 700 else 32
	
	def should_rotate(self, orientation):
		return True
	
	def touch_began(self, touch):
		if self.show_instructions:
			self.show_instructions = False
			blend_mode(BLEND_ADD)
	
	def touch_moved(self, touch):
		if len(self.particles)<50:
			particle = Particle(touch.location)
			self.particles.add(particle)
	
	def draw(self):
		background(0, 0, 0)
		if self.show_instructions:
			s = 40 if self.size.w > 700 else 17
			text('Move your fingers across the screen.',
			     'Futura', s, *self.bounds.center().as_tuple())
		dead = set()
		newParts=set()
		for particle in self.particles:
			r, g, b = hsv_to_rgb(particle.hue, 1, 1)
			a = particle.alpha
			tint(r * a, g * a, b * a, a)
			x, y = particle.location.as_tuple()
			s = a * self.p_size# (1.01 - a) * self.p_size
			image('White_Circle', x - s/2, y - s/2, s, s)
			particle.alpha -= 0.0001
			#particle.hue += 0.001
			particle.location.x += particle.velocity.w
			particle.location.y += particle.velocity.h
			particle.velocity.h-=grav
			if particle.location.x>=self.size.w:
				particle.location.x=self.size.w
				particle.velocity.w*=(-1+inertia)
			elif particle.location.x<=0:
				particle.location.x=0
				particle.velocity.w*=(-1+inertia)
			if particle.location.y>=self.size.h:
				particle.location.y=self.size.h
				particle.velocity.h*=(-1+inertia)
			elif particle.location.y<=0:
				particle.location.y=0
				particle.velocity.h*=(-1+inertia)
			#Hit test
			for i in self.particles:
				if not i==particle:
					s2=i.alpha*self.p_size
					test=hitCircles(particle.location.x,particle.location.y,s,
					                i.location.x,i.location.y,s2)
					if test:
						i.velocity.w=test[0]*.1
						particle.velocity.w=(test[0]*-1)*.1
					 	i.velocity.h=test[1]*.1
					 	particle.velocity.h=(test[1]*-1)*.1
					 	if s2>s: 
					 		particle.alpha-=.1
					 		i.alpha-=.05
					 		particle.hue=i.hue
					 	else: 
					 		i.alpha-=.1
					 		particle.alpha-=.05
					 		i.hue=particle.hue
			if particle.alpha <= .1:# or particle.location.x>=self.size.w:
				dead.add(particle)
		self.particles -= dead
		#for particle in newParts:
		#	particle.velocity=Size(random() * 4 - 2, random() * 4 - 2)
		#	self.particles.add(particle)

run(Particles())