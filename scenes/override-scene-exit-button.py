# coding: utf-8

# Captured from: _https://forum.omz-software.com/topic/2519/override-scene-exit-button

import scene, ui

class UnclosableScene(ui.View):
	def __init__(self, the_scene):
		scene_view = scene.SceneView()
		scene_view.scene = the_scene
		self.present(hide_title_bar=True)
		scene_view.frame = self.bounds
		self.add_subview(scene_view)
		
class BlueScene(scene.Scene):
	def __init__(self):
		self.background_color = 'midnightblue'
		
UnclosableScene(BlueScene())

