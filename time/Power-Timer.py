# https://gist.github.com/spencerogden/4704842

# Stopwatch
#
# A simple stopwatch that demonstrates the scene module's text
# drawing capabilities.

from scene import *
from math import modf, floor
from itertools import chain
import string
import sound
import time

class Stopwatch (Scene):
	def setup(self):
		self.start_time = 0.0
		self.intro = 5
		self.stop_time = 0.0
		self.last_seconds = 0
		self.running = False
		for effect in ['Click_1', 'Click_2','Boing_1','Beep']:
			sound.load_effect(effect)
	
	def should_rotate(self, orientation):
		return False
	
	def draw(self):
		background(0, 0, 0)
		#Format the elapsed time (dt):
		dt = 0.0
		if self.running:
			dt = (time.time() - self.start_time)
		else:
			dt = (self.stop_time - self.start_time)
		minutes = abs(dt) / 60
		seconds = abs(dt) % 60
		centiseconds = modf(abs(dt))[0] * 100
		if floor(dt) != self.last_seconds:
			if floor(dt) == 0:
				sound.play_effect('Beep')
				time.sleep(.1)
				sound.play_effect('Beep')
			elif floor(dt) % 10 == 0:
				sound.play_effect('Beep')
			else: 
				sound.play_effect('Click_1')
			self.last_seconds = floor(dt)
		s = '%02d:%02d.%02d' % (minutes, seconds, centiseconds)
		reps = 'Reps: %d' % (dt/20)
		text(reps, 
		     x=self.size.w * 0.5,
		     y=self.size.h * 0.7,
		     font_size=48)
		text(s,
		     x=self.size.w * 0.5,
		     y=self.size.h * 0.4,
		     font_size=64)

	
	def touch_began(self, touch):
		if not self.running:
			if self.start_time > 0:
				#Reset:
				self.start_time = 0.0
				self.last_seconds = 0
				self.stop_time = 0.0
			else:
				#Start:
				self.start_time = time.time()+self.intro
				self.running = True
		else:
			#Stop:
			self.stop_time = time.time()
			self.running = False

run(Stopwatch())
