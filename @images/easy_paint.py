from scene import *

class MyScene (Scene):
	def setup(self):
		self.xybegin = Point(0,0)
		self.lines = []
	
	def draw(self):
		background(0, 0, 0)
		fill(0, 0, 1)
		stroke(0, 0, 1)
		stroke_weight(3)

		for l in self.lines:
			line(*l)
			
		text(str(len(self.lines)), x=100,y=100)
		
	def touch_began(self, touch):
		x = touch.location.x
		y = touch.location.y
		self.xybegin = Point(x,y)
	
	def touch_moved(self, touch):
			x = touch.location.x
			y = touch.location.y
			ppos = touch.prev_location
			self.lines.append((ppos.x, ppos.y, x, y))

	def touch_ended(self, touch):
		x = touch.location.x
		y = touch.location.y
		ppos = touch.prev_location
		self.lines.append((ppos.x, ppos.y, x, y))
		
run(MyScene())
