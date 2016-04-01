# https://gist.github.com/omz/4059061

# Quick-and-dirty demo of how to run multiple scenes
# in Pythonista; The MultiScene class is basically a
# wrapper for another scene and forwards all events
# to the currently-active scene, which can be changed
# with the switch_scene method.
# 
# In this example, the first scene simply draws a red
# background and switches to the second scene when a
# touch is detected. The second scene draws a green
# background and plays a beep sound on touch.

from scene import *
import sound

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

class Scene1 (Scene):
	def draw(self):
		background(1, 0, 0)
	def touch_began(self, touch):
		# Switch to Scene2:
		main_scene.switch_scene(Scene2())

class Scene2 (Scene):
	def draw(self):
		background(0, 1, 0)
	def touch_began(self, touch):
		sound.play_effect('Beep')

# Start with Scene1:
main_scene = MultiScene(Scene1())
run(main_scene)