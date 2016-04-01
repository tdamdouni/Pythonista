# randomized_timer.py
#
# A simple app to conduct randomized time trials based on the Stopwatch.py 
# sample app in [Pythonista](http://omz-software.com). 
#
# This script takes an array of choices (strings) and randomly selects one on 
# launch in Pythonista. You then tap the screen to start a stopwatch and tap it
# again to stop it. When you tap it a third time, the choice presented to you 
# plus the elapsed time in seconds are added to a callback URL to call a 
# separate script in the iOS [Workflow](https://workflow.is/) app for further 
# processing. 
#
# The workflow I use with the Workflow app is availanble here: 
# https://workflow.is/workflows/813286b8841d4688945f7c2bbdff74db
#
# You can set up your choices by modifying the elements in the array for 
# self.route in the setup function for the Stopwatch class.

from scene import *
from time import time
from math import modf
from itertools import chain
import string
import webbrowser
from numpy.random import choice

class Stopwatch (Scene):
	def setup(self):
		self.start_time = 0.0
		self.stop_time = 0.0
		self.running = False
		self.route = choice(['Light', 'NON-light'])
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
		text(self.route, font_size=48.0,x = 100, y=500)
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
				export_time = self.stop_time - self.start_time
				self.start_time = 0.0
				self.stop_time = 0.0
				
				url = 'workflow://x-callback-url/run-workflow?name=route_time&input=text&text=' + self.route + '%20' + str(export_time)
				webbrowser.open(url)
			else:
				#Start:
				self.start_time = time()
				self.running = True
		else:
			#Stop:
			self.stop_time = time()
			self.running = False

run(Stopwatch())
