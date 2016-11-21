# https://forum.omz-software.com/topic/3306/disable-on-screen-printing-in-scene-sceneview

from objc_util import ObjCInstance
ObjCInstance(self.view).statusLabel().alpha = 0

setup# --------------------
from objc_util import ObjCInstance
ObjCInstance(self.view).statusLabel().alpha = 0
# --------------------
View.present(hide_title_bar=True)# --------------------
ui# --------------------
from scene import *

def run2(scn):
	sv = SceneView()
	sv.scene = scn
	sv.present(hide_title_bar=True)
	
run2(Scene())
# --------------------
import scene, ui

class MyScene(scene.Scene):
	def setup(self):
		self.label = scene.LabelNode('Test hide title bar',
		position=self.size/2, parent=self)
		
#scene.run(MyScene())

'''
# This does not hide the close button
scene_view = scene.SceneView()
scene_view.scene = MyScene()
scene_view.present('fullscreen', hide_title_bar=True)
'''

# This works
v = ui.View()
scene_view = scene.SceneView()
scene_view.flex= 'WH'
scene_view.scene = MyScene()
v.add_subview(scene_view)
v.present('fullscreen', hide_title_bar=True)

# --------------------
class MyScene(scene.Scene):
	def setup(self):
		self.label = scene.LabelNode('Test hide title bar',
		position=self.size/2, parent=self)
		self.hide_close()
		
	def hide_close(self, state=True):
		from obj_util import ObjCInstance
		v = ObjCInstance(self.view)
		# Find close button.  I'm sure this is the worst way to do it
		for x in v.subviews():
			if str(x.description()).find('UIButton) >= 0:
				x.setHidden(state)
				
scene.run(MyScene())

# --------------------
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


# --------------------

