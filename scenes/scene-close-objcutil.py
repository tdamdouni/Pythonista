# https://forum.omz-software.com/topic/3306/disable-on-screen-printing-in-scene-sceneview/9

import scene
import objc_util

class MyScene(scene.Scene):
	def setup(self):
		self.label = scene.LabelNode('Test hide title bar',
		position=self.size/2, parent=self)
		self.hide_close()
		
	def hide_close(self, state=True):
		from objc_util import ObjCInstance
		v = ObjCInstance(self.view)
		# Find close button.  I'm sure this is the worst way to do it
		for x in v.subviews():
			if str(x.description()).find('UIButton >= 0'):
				x.setHidden(state)
				
scene.run(MyScene())

