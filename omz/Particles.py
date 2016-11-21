# Particles
#
# Create colorful bubbles by moving your fingers.

from scene import *
from random import random
from colorsys import hsv_to_rgb

class Particle (object):
	def __init__(self, location):
		self.velocity = Size(random() * 4 - 2, random() * 4 - 2)
		self.location = location
		self.hue = random()
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
		particle = Particle(touch.location)
		self.particles.add(particle)
	
	def draw(self):
		background(0, 0, 0)
		if self.show_instructions:
			s = 40 if self.size.w > 700 else 17
			text('Move your fingers across the screen.',
			     'Futura', s, *self.bounds.center().as_tuple())
		dead = set()
		for particle in self.particles:
			r, g, b = hsv_to_rgb(particle.hue, 1, 1)
			a = particle.alpha
			tint(r * a, g * a, b * a, a)
			x, y = particle.location.as_tuple()
			s = (2 - a) * self.p_size
			image('White_Circle', x - s/2, y - s/2, s, s)
			particle.alpha -= 0.02
			particle.hue += 0.02
			particle.location.x += particle.velocity.w
			particle.location.y += particle.velocity.h
			if particle.alpha <= 0:
				dead.add(particle)
		self.particles -= dead

run(Particles())
