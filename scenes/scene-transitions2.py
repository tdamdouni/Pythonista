# https://forum.omz-software.com/topic/2500/scene-transitions

# for use with https://github.com/omz/PythonistaAppTemplate

from scene import *
import ui

class MainScene (Scene):
	def setup(self):
		# this is the starting scene, for ui.View
		# all other scenes will come from
		
		self.background_color = 'black'
		self.present_modal_scene(first_scene)
		
		
class FirstScene (Scene):
	def setup(self):
		# add background color
		self.background = SpriteNode(color = 'white')
		self.background.size = self.size
		self.background.position = self.size / 2
		self.add_child(self.background)
		
		self.ship = SpriteNode('spc:PlayerShip1Orange')
		self.ship.position = self.size / 2
		self.add_child(self.ship)
		
	def update(self):
		pass
	#x, y, z = gravity()
	#pos = self.ship.position
	#pos += (x * 15, y * 15)
	# Don't allow the ship to move beyond the screen bounds:
	#pos.x = max(0, min(self.size.w, pos.x))
	#pos.y = max(0, min(self.size.h, pos.y))
	#self.ship.position = pos
	
	def touch_began(self, touch):
		# question?
		# how do you get to the second scene?
		#self.dismiss_modal_scene()
		self.present_modal_scene(second_scene)
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		pass
		
		
class SecondScene (Scene):
	def setup(self):
		# add background color
		self.background = SpriteNode(color = 'green')
		self.background.size = self.size
		self.background.position = self.size / 2
		self.add_child(self.background)
		
		self.ship = SpriteNode('spc:EnemyGreen2')
		self.ship.position = self.size / 2
		self.add_child(self.ship)
		
	def touch_began(self, touch):
		self.present_modal_scene(first_scene)
#pass


main_scene = MainScene()
first_scene = FirstScene()
second_scene = SecondScene()
# Instead of...
# run(MyScene())

# ..use:
main_view = ui.View()
scene_view = SceneView(frame=main_view.bounds, flex='WH')
main_view.add_subview(scene_view)
scene_view.scene = first_scene
main_view.present(hide_title_bar=True, animated=False)

