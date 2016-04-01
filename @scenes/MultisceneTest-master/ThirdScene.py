# Scene3

from scene import *
import sound

from scene_manager import *

class Scene3 (Scene):
	def draw(self):
		background(0, 0, 1)
	def touch_began(self, touch):
		sound.play_effect('Clank')
		main_scene.switch_scene(Scene1())
