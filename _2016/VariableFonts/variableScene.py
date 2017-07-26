# https://github.com/dyyybek/pythonista/tree/master/VariableFonts

# https://forum.omz-software.com/topic/3946/how-to-improve-speed-of-drawing-very-slow-scene-view/4

from scene import *
from pathsLists import *
from variableTools import *

import ui

glyphsDict = glyphsDictConstruct(l)

class MyScene (Scene):
	def setup(self):

		self.myPath = ShapeNode(glyphsDict[1])
		self.myPath.anchor_point = 0,0
		self.myPath.position = 1024 - self.myPath.bbox.width*1.75 ,768 - self.myPath.bbox.height*1.3
		self.add_child(self.myPath)
		
		self.background_color = 'lightgrey'
		
	def touch_began(self, touch):
		x, y = touch.location
		z = int(x/(10.24/2)+1)
		self.myPath.path = glyphsDict[z]
	def touch_moved(self, touch):
		x, y = touch.location
		z = int(x/(10.24/2)+1)
		self.myPath.path = glyphsDict[z]
run(MyScene(), show_fps=True)
