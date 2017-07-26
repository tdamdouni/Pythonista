from scene import *
from random import random

class MyScene (Scene):
	def setup(self):
		# This will be called before the first frame is drawn.
		self.root_layer = Layer(self.bounds)
		self.mLines = []
		self.mCount = 0
		(self.mCurrLocX, self.mCurrLocY) = self.bounds.center()
		stroke_weight(2)
		stroke(0, 0, 0.5)
		
	def draw(self):
		# Update and draw our root layer. For a layer-based scene, this
		# is usually all you have to do in the draw method.
		currLoc = Point(self.mCurrLocX, self.mCurrLocY)
		if currLoc in self.bounds: # and len(self.mLines) < 8:
			lineLength = (self.mCount + 2) / 2 * 4 # 4, 4, 8, 8, 12, 12...
			theDirection = self.mCount % 4 # 0=E, 1=S, 2=W, 3=N
			self.mCount += 1               # turn right 90 degrees
			startLocX = self.mCurrLocX
			startLocY = self.mCurrLocY
			if theDirection == 0:   # head East
				self.mCurrLocX += lineLength
			elif theDirection == 1: # head South
				self.mCurrLocY -= lineLength
			elif theDirection == 2: # head West
				self.mCurrLocX -= lineLength
			else:                   # head North
				self.mCurrLocY += lineLength
			self.mLines.append((startLocX, startLocY,
			self.mCurrLocX, self.mCurrLocY))
		for theLine in self.mLines:
			line(theLine[0], theLine[1], theLine[2], theLine[3])
			
	def touch_began(self, touch):
		pass
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		pass
		
run(MyScene())

