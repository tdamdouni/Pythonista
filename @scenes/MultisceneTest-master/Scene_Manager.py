# Quick-and-dirty demo of how to run multiple scenes
# in Pythonista; The MultiScene class is basically a
# wrapper for another scene and forwards all events
# to the currently-active scene, which can be changed
# with the switch_scene method.

from scene import *

class MultiScene (Scene):
	def __init__(self, start_scene):
		self.active_scene = start_scene
	def switch_scene(self, new_scene):
		self.active_scene = new_scene
		new_scene.setup()
	def draw(self):
		self.active_scene.draw()
	def touch_began(self, touch):
		self.active_scene.touch_began(touch)
	def touch_moved(self, touch):
		self.active_scene.touch_moved(touch)
	def touch_ended(self, touch):
		self.active_scene.touch_ended(touch)
