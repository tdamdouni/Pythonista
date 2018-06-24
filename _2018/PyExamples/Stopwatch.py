# Stopwatch
#
# A simple stopwatch that demonstrates the scene module's text
# drawing capabilities.

from scene import *
from time import time
from math import modf
from itertools import chain
import string

class Stopwatch (Scene):
	def setup(self):
		self.start_time = 0.0
		self.stop_time = 0.0
		self.running = False
		#Render all the digits as individual images:
		self.numbers = {}
		font_size = 150 if self.size.w > 700 else 60
		for s in chain(string.digits, [':', '.']):
			#render_text returns a tuple of
			#an image name and its size.
			self.numbers[s] = render_text(s, 'Helvetica-Bold', font_size)
	
	def should_rotate(self, orientation):
		return True
	
	def draw(self):
		background(0, 0, 0)
		#Format the elapsed time (dt):
		dt = 0.0
		if self.running:
			dt = time() - self.start_time
		else:
			dt = self.stop_time - self.start_time
		minutes = dt / 60
		seconds = dt % 60
		centiseconds = modf(dt)[0] * 100
		s = '%02d:%02d.%02d' % (minutes, seconds, centiseconds)
		#Determine overall size for centering:
		w, h = 0.0, self.numbers['0'][1].h
		for c in s:
			size = self.numbers[c][1]
			w += size.w
		#Draw the digits:
		x = int(self.size.w * 0.5 - w * 0.5)
		y = int(self.size.h * 0.5 - h * 0.5)
		for c in s:
			img, size = self.numbers[c]
			image(img, x, y, size.w, size.h)
			x += size.w
	
	def touch_began(self, touch):
		if not self.running:
			if self.start_time > 0:
				#Reset:
				self.start_time = 0.0
				self.stop_time = 0.0
			else:
				#Start:
				self.start_time = time()
				self.running = True
		else:
			#Stop:
			self.stop_time = time()
			self.running = False

run(Stopwatch())
