# https://forum.omz-software.com/topic/3306/disable-on-screen-printing-in-scene-sceneview/7

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

