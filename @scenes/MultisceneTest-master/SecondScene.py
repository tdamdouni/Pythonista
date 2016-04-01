# Scene2

from scene import *
import sound

from scene_manager import *

class Scene2 (Scene):
	def draw(self):
		background(0, 1, 0)
	def touch_began(self, touch):
		sound.play_effect('Beep')
		main_scene.switch_scene(Scene3())
