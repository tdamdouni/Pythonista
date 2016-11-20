# Tea timer for Pythonista
# ========================================
# ThreeMinutes is a simple to use team timer.
# The timer can be set to every time in minute range.
# The time is changed by swiping up and down.
# A single touch starts/stopps the timer.
# You are reminded by an alarm that your tea is ready.
# 
# This script was inspired by the Pythonistas
# stopwatch example.
#
# Get Pythonista for iOS from
# http://omz-software.com/pythonista/
#
# Done by bitscribble 2013-02-04
#

# KNOWN PROBLEMS
# - script does not alert the user if the timer runs out and the iOS device suspends



# TODO
# - redefine enums for gestures in a nicer way
# - encapsulate the alarm stuff (screen blinking, alarm sound)
# - clean up the dirty code that mixes up drawing and calculating
# - put gesture evaluation in external library (class)
# - clean all magic values and put them in an extra class

from scene import *
from time import time
from math import modf
from itertools import chain
import string
import sound

# define enum like class for recognized gestures (user input)
class Gesture():
	TAP = 'tap'
	UP = 'up'
	DOWN = 'down'

# the basic scene class for the tea timer
class ThreeMinutes (Scene):


	# the setup method is called once at the beginning	
	def setup(self):
		
		sound.load_effect('Beep')
		sound.set_volume(1.0)
		self.alarm_timer = 0
		self.bg_red = True
		
		self.timer = 180
		self.start_time = 0.0
		self.running = False
		self.dt = 0.0
		self.alert = False
		
		# gesture recognition
		self.gesture = Gesture.TAP
		self.start_touches = {}
		self.touch_count = {}
		
		#Render all the digits as individual images:
		self.numbers = {}
		font_size = 200 if self.size.w > 700 else 100
		for s in chain(string.digits, [':', '.']):
			#render_text returns a tuple of
			#an image name and its size.
			self.numbers[s] = render_text(s, 'Helvetica-Bold', font_size)
	
	def should_rotate(self, orientation):
		return True
	
	def draw(self):
		# draw the backgound (black/red)
		if self.alert == True:
			self.draw_alert_background()
			self.play_alarm()
		else:
			background(0,0,0)
		
		#Format the elapsed time (dt/duration time):
		if self.running:
			# calculate the duration time
			self.dt = self.timer - (time() - self.start_time)
			# the timer eleapsed
			if self.dt < 0.00:
				# set the timer to 0.0 tp avoid negative values
				self.dt = 0.0
				self.alert = True
		else:
			# if we are not running, simply print the timer on the screen
			self.dt = self.timer
		
		# draw the timer to the display
		self.draw_digits(self.dt)


	def touch_began(self, touch):
		# copy every new touch in our startpoint register
		self.start_touches[touch.touch_id] = touch
		self.touch_count[touch.touch_id] = 1

	
	def touch_moved(self, touch):
		# increment touches by one
		self.touch_count[touch.touch_id] = self.touch_count[touch.touch_id] + 1

		
	def touch_ended(self, touch):
		# increment touchcounter and save it for the drawing method
		# and gesture recognition
		self.touch_count[touch.touch_id] = self.touch_count[touch.touch_id] + 1
		# for easier access
		touch_count = self.touch_count[touch.touch_id]
		
		# save first and last touch for gesture recognition
		firsttouch = self.start_touches[touch.touch_id]
		lasttouch = touch
		
		self.gesture = self.recognize_gesture(firsttouch.location.x, firsttouch.location.y, \
		                                 lasttouch.location.x, lasttouch.location.y, touch_count)

		# start/reset the timer with a simple tap (single touch)
		if self.gesture == Gesture.TAP:
			# run the timer if it is not running
			if not self.running:
				self.start_time = time()
				self.running = True
			else:
				self.running = False
				# reset alert
				self.alert = False
				# reset alarm timer
				self.alarm_timer = 0
				# begin with red blinking at next alarm again
				self.bg_red = True

		# increment the timer by one minute if the user swipes up
		# (only available if the timer is not running at the moment)
		if self.gesture == Gesture.UP:
			if not self.running:
					self.timer = self.timer + 60 # add one minute to timer

		# decrement the timer by one minute if the user swipers down
		# (also not available while running)
		if self.gesture == Gesture.DOWN:
			if not self.running:
				# only decrement timer by one minute if at least two minutes are left
				if self.timer >= 120:
					self.timer = self.timer - 60
		
		
	# this function draws the digits
	def draw_digits(self, dig):
		# seperate the minutes and seconds from the duration time
		minutes = dig / 60
		seconds = dig % 60
		
		# format the digits into a string
		s = '%02d:%02d' % (minutes, seconds)
		
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

			
	def recognize_gesture(self, x1, y1, x2, y2, touches):
		gesture = Gesture.TAP
		# only calc gesture for touches with a bridge
		# if there is only a beginning and an end,
		# we define it as a single touch
		if touches > 2:
			if y1 > y2:
				gesture = Gesture.DOWN
			else:
				gesture = Gesture.UP
		return gesture

	def play_alarm(self):
		if self.alarm_timer == 0:
			sound.play_effect('Beep')
			self.alarm_timer = 30 # two times every second
		else:
			self.alarm_timer = self.alarm_timer - 1
			
	def draw_alert_background(self):
		if self.alarm_timer == 0:
			# change background
			if self.bg_red:
				background(1,0,0)
				self.bg_red = False
			else:
				background(0,0,0)
				self.bg_red = True

run(ThreeMinutes())
