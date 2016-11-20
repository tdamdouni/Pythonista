# Small gesture testing script for Pythonista
# ========================================
# At this time only up, down and simple tap
# gesture is recognized.
#
# Get Pythonista for iOS from
# http://omz-software.com/pythonista/
#
# Done by bitscribble 2013-01-25

from scene import *

class UpDownGestureTest (Scene):
	def setup(self):
		# This will be called before the first frame is drawn.
		# create a list with start points of actual touches
		self.start_touches = {}
		self.touch_count = {}
		self.lastgesture = 'na'
		self.dist_x = 0
		self.last_count = 0
		
	def draw(self):
		# This will be called for every frame (typically 60 times per second).
		background(0, 0, 0)
		# Draw a red circle for every finger that touches the screen:
		fill(1, 0, 0)
		
		# Write a simple log about the screen size and the application
		self.simpletext('Gesture Test\n\nW:' + str(self.size.w) + '\nH: ' + \
		str(self.size.h), 0, self.size.h-90, 20)
		# writhe down the last recognized gesture (none by default)
		self.simpletext(self.lastgesture, 0, (self.size.h/2.0)-40, 80)
		# distance between touch start and end
		self.simpletext('Distance: '+str(self.dist_x), 0,20,20)
		# counter of single touches recognized by pythonista
		self.simpletext('Touches:  '+str(self.last_count), 0,0,20)
		stroke(1,1,1)
		stroke_weight(2)
		line(220, self.size.h, 220, 0)
		
		for touch in self.touches.values():
			ellipse(touch.location.x - 50, touch.location.y - 50, 100, 100)
			# draw touch id above the circle
			self.simpletext(touch.touch_id, touch.location.x-50, touch.location.y+50, 20)
			# draw touch location under the circle
			self.simpletext(str(touch.location.x)+' ,'+str(touch.location.y), \
			touch.location.x-50, touch.location.y-70,20)
			
		# clear list of startpoints of none are existing
		if len(self.touches) == 0:
			self.start_touches = {}
			self.touch_count = {}
			
	def touch_began(self, touch):
		# copy every new touch in our startpoint register
		self.start_touches[touch.touch_id] = touch
		self.touch_count[touch.touch_id] = 1
		
	def touch_moved(self, touch):
		self.touch_count[touch.touch_id] = self.touch_count[touch.touch_id] + 1
		
	def touch_ended(self, touch):
		# increment touchcounter and save it for the drawing method
		# and gesture recognition
		self.touch_count[touch.touch_id] = self.touch_count[touch.touch_id] + 1
		self.last_count = self.touch_count[touch.touch_id]
		
		# save first and last touch for gesture recognition
		firsttouch = self.start_touches[touch.touch_id]
		lasttouch = touch
		
		# fetch the calculated gesture for the drawing method
		self.lastgesture = \
		GestureUtils.touch_direction(self.size.w, self.size.h, \
		firsttouch.location.x, firsttouch.location.y, \
		lasttouch.location.x, lasttouch.location.y, self.last_count)
		
		# calculate he distance between the two touches (height only)
		self.dist_x = \
		GestureUtils.distance(firsttouch.location.x, firsttouch.location.y, \
		lasttouch.location.x, lasttouch.location.y)
		
	# simple method to print text onto screen in easy way
	def simpletext(self, text, x, y, size):
		img, size = render_text(text, 'Helvetica-Bold', size)
		image(img, x, y, size.w, size.h)
		
		
class GestureUtils():

	# returns up, down, na (simple touch)
	@staticmethod
	def touch_direction(screen_w, screen_h, x1, y1, x2, y2, touches):
		retval = 'na'
		# only calc gesture for touches with a bridge
		# if there is only a beginning and an end,
		# we define it as a single touch
		if touches > 2:
			if y1 > y2:
				retval = 'down'
			else:
				retval = 'up'
		return retval
		
	# calculates the distance between the two touches
	@staticmethod
	def distance(x1, y1, x2, y2):
		retval_x = 0
		if x1 > x2:
			retval_x = x1 - x2
		else:
			retval_x = x2 - x1
		return retval_x
		
run(UpDownGestureTest())

