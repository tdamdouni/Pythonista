# https://forum.omz-software.com/topic/3946/how-to-improve-speed-of-drawing-very-slow-scene-view

from scene import *
import ui

glyphsDict = {}  # My dictionary with paths to draw

class MyScene (Scene):
	def setup(self):
	
		self.myPath = ShapeNode(glyphsDict[1])  # first path to draw
		self.add_child(self.myPath)
		
		self.background_color = 'lightgrey'
		
	def touch_began(self, touch):
		x, y = touch.location
		z = int(x/(10.24/2)+1)
		self.myPath.path = glyphsDict[z]  # Setting a new path to draw
		
	def touch_moved(self, touch):
		x, y = touch.location
		z = int(x/(10.24/2)+1)
		self.myPath.path = glyphsDict[z]  # Setting a new path to draw
		
run(MyScene())

