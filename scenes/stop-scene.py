# https://forum.omz-software.com/topic/3477/how-to-stop-scene

import scene, ui

class MyScene(scene.Scene):
	def setup(self):
		self.test_label = scene.LabelNode('Hello World',
		position=self.size/2.0, parent=self)
		self.close_label = scene.LabelNode('Close scene',
		position=(self.size[0]/2, self.size[1]/2-100),
		parent=self)
		
	def touch_began(self, touch):
		if touch.location in self.close_label.frame:
			self.view.close()
			
scene.run(MyScene())

