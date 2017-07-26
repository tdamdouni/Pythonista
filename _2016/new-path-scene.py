# https://forum.omz-software.com/topic/3946/how-to-improve-speed-of-drawing-very-slow-scene-view/9

import scene
from variableTools import glyphsListConstruct

glyphs_list1 = glyphsListConstruct()
reduction_factor = 4.0
x_factor = (10.24 / 2)*reduction_factor


class MyScene(scene.Scene):
	def setup(self):
		self.glyphs_list = [scene.ShapeNode(i) for i in glyphs_list1[::int(reduction_factor)]]
		self.myPath = self.glyphs_list[0]
		self.myPath.anchor_point = 0, 0
		self.myPath.position = (1024 - self.myPath.bbox.width * 1.75,
		768 - self.myPath.bbox.height * 1.3)
		self.add_child(self.myPath)
		self.background_color = 'lightgrey'
		self.touch_moved = self.touch_began
		
	def touch_began(self, touch):
		r = int(touch.location.x / x_factor)%len(self.glyphs_list)
		#print(touch.location.x, r)
		self.myPath.remove_from_parent()
		self.myPath = self.glyphs_list[r]
		self.myPath.anchor_point = 0, 0
		self.myPath.position = (1024 - self.myPath.bbox.width * 1.75,
		768 - self.myPath.bbox.height * 1.3)
		self.add_child(self.myPath)
		
		
scene.run(MyScene(), show_fps=True)

