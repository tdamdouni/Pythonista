# For use in pythonista on iOS
# Displays user (non-gravity) acceleration component and visually
# records the high water mark.  Tap in center of circle to reset.

import motion
from scene import *

scale = 100 # scale raw accelerometer values to screen

class MyScene (Scene):

	def setup(self):
		motion.start_updates()
		self.x = self.size.w * 0.5
		self.y = self.size.h * 0.5
		self.cx = self.x
		self.cy = self.y
		self.max = 0

	def touch_ended(self, touch):
	  # Resets max acceleration indicator when center dot is tapped
		frame = Rect(self.cx-15, self.cy-15, 30, 30)
		if touch.location in frame:
			self.max = 0

	def draw(self):
		ac = motion.get_user_acceleration()
		self.x = (ac[0] * scale) + self.cx
		self.y = (ac[1] * scale) + self.cy
		# clip to screen
		self.x = min(self.size.w - 10, max(0, self.x)) 
		self.y = min(self.size.h - 100, max(0, self.y))
		# save if biggest acceleration so far
		self.max = max(self.max, max(abs(ac[0]*scale), abs(ac[1]*scale)))
		# redraw screen
		background(1, 1, 1)
		# show max accel ring
		fill(1,1,1)
		stroke(0,0,0)
		stroke_weight(1)
		ellipse(self.cx-self.max, self.cy-self.max, self.max*2, self.max*2)
		# center dot
		fill(0, 0, 0)
		rect(self.cx, self.cy, 2, 2)
		# cur accel
		fill(1, 0, 0)
		rect(self.x, self.y, 10, 10)
		# print accel value
		tint(0, 0, 0)
		text(str(self.max), 'Helvetica', 16, 50, 50, 6)

run(MyScene())
