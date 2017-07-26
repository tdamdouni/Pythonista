# https://forum.omz-software.com/topic/1487/is-it-possible-to-hide-the-stop-cross-in-the-upper-lefthand-corner/4

import scene, ui
from objc_util import UIApplication

def close_view():
	v.close()
	
class MyScene(scene.Scene):
	def setup(self):
		self.test_label = scene.LabelNode('Test hide title bar',
		position=self.size/2.0, parent=self)
		self.close_label = scene.LabelNode('Close view',
		position=(self.size[0]/2, self.size[1]/2-100),
		parent=self)
		
	def touch_began(self, touch):
		if touch.location in self.close_label.frame:
			close_view()
			
w, h = ui.get_window_size()
frame = (0, 0, w, h)
v = ui.View(frame=frame)
scene_view = scene.SceneView(frame=frame)
scene_view.flex= 'WH'
scene_view.scene = MyScene()
v.add_subview(scene_view)
v.present('fullscreen', hide_title_bar=True)
UIApplication.sharedApplication().statusBar().hidden = True

