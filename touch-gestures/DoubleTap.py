from scene import *
from time import time
import sound

MAX_DOUBLE_TAP_DELAY = 0.25

class DoubleTapScene (Scene):
	def setup(self):
		self.last_touch_up_time = 0
		self.double_tap_start_time = 0
		
	def touch_ended(self, touch):
		if time() - self.last_touch_up_time < MAX_DOUBLE_TAP_DELAY:
			sound.play_effect('Beep')
			self.double_tap_start_time = time()
			self.last_touch_up_time = 0
		else:
			self.last_touch_up_time = time()
			
	def draw(self):
		background(0, 0, 0)
		# Show message if a double-tap was detected:
		if self.double_tap_start_time > 0:
			text('Double Tap!', 'Helvetica', 50, self.size.w/2, self.size.h/2)
			# Hide the message after 1 second:
			if time() - self.double_tap_start_time > 1.0:
				self.double_tap_start_time = 0
				
run(DoubleTapScene())

