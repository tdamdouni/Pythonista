# Scene1

from scene import *
import sound

from scene_manager import *

class Scene1 (Scene):
	def draw(self):
		background(1, 0, 0)
	def touch_began(self, touch):
		sound.play_effect('Coin_1')
		main_scene.switch_scene(Scene2())
