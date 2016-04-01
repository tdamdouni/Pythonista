# Clock
#
# An analog clock that demonstrates drawing basic
# shapes with the scene module.

from scene import *
from time import localtime

ipad = False #will be set in the setup method

#Our Clock class inherits from Scene, so that its draw method
#is automatically called 60 times per second when we run it.
class Clock (Scene):
	def setup(self):
		global ipad
		ipad = self.size.w > 700
	
	def should_rotate(self, orientation):
		return True
	
	def draw(self):
		background(0, 0.2, 0.3)
		t = localtime()
		minute = t.tm_min
		second = t.tm_sec
		hour = t.tm_hour % 12
		margin = 25 if ipad else 5
		r = (min(self.size.w, self.size.h) / 2) - margin * 2
		center = Point(self.size.w/2, self.size.h/2)
		#Draw the clock face:
		fill(0.8, 0.8, 0.8)
		stroke(0.5, 0.5, 0.5)
		line_w = 10 if ipad else 5
		stroke_weight(line_w)
		ellipse(center.x - r, center.y - r, r*2, r*2)
		#Draw 12 markers for the hours:
		push_matrix()
		fill(0.5, 0.5, 0.5)
		no_stroke()
		translate(center.x, center.y)
		digit_w = 20 if ipad else 10
		digit_h = 40 if ipad else 20
		for i in xrange(12):
			rotate(30)
			rect(-digit_w/2, r-digit_h, digit_w, digit_h)
		pop_matrix()
		#Draw the minute hand:
		push_matrix()
		translate(center.x, center.y)
		rotate((-360 / 60) * minute + (-360/60) * (second/60.))
		fill(0, 0, 0)
		m_height = r - (60 if ipad else 30)
		m_width = 20 if ipad else 10
		rect(-m_width/2, -m_width/2, m_width, m_height)
		pop_matrix()
		#Draw the hour hand:
		push_matrix()
		translate(center.x, center.y)
		rotate((-360 / 12) * hour + (-360/12.) * (minute/60.))
		fill(0, 0, 0)
		h_width = 20 if ipad else 10
		h_height = r - (120 if ipad else 60)
		rect(-h_width/2, -h_width/2, h_width, h_height)
		pop_matrix()
		#Draw the second hand:
		push_matrix()
		translate(center.x, center.y)
		rotate((-360 / 60) * second)
		fill(1, 0, 0)
		s_width = 10 if ipad else 6
		s_height = r - (60 if ipad else 20)
		rect(-s_width/2, -s_width/2, s_width, s_height)
		pop_matrix()
		fill(0, 0, 0)
		#Draw the small circle in the middle:
		r = 20 if ipad else 10
		ellipse(center.x - r, center.y - r, r*2, r*2)

#Run the scene that we just defined:
run(Clock())
