# In this example, the program moved between 3 different scenes.

from scene import *
import sound

from Scene_Manager import *

# would like to remove the following 3 scenes and place then in seperate files
class Scene1 (Scene):
	def draw(self):
		background(1, 0, 0)
	def touch_began(self, touch):
		sound.play_effect('Coin_1')
		main_scene.switch_scene(Scene2())

class Scene2 (Scene):
	def draw(self):
		background(0, 1, 0)
	def touch_began(self, touch):
		sound.play_effect('Beep')
		main_scene.switch_scene(Scene3())
		
class Scene3 (Scene):
	def draw(self):
		background(0, 0, 1)
	def touch_began(self, touch):
		sound.play_effect('Clank')
		main_scene.switch_scene(Scene1())

# Start with Scene1:
main_scene = MultiScene(Scene1())
run(main_scene, orientation= LANDSCAPE)
