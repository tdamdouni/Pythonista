# https://forum.omz-software.com/topic/2500/scene-transitions/20

from scene import *

class FirstScene(Scene):
	def setup(self):
		# add white background
		SpriteNode(anchor_point=(0, 0), color='white', parent=self,
		size=self.size)
		self.ship = SpriteNode('spc:PlayerShip1Orange', parent=self,
		position=self.size / 2)
		
	def touch_began(self, touch):
		self.present_modal_scene(second_scene)
		
		
class SecondScene(Scene):
	def setup(self):
		# add green background
		SpriteNode(anchor_point=(0, 0), color='green', parent=self,
		size=self.size)
		self.ship = SpriteNode('spc:EnemyGreen2', parent=self,
		position=self.size / 2)
		
	def touch_began(self, touch):
		self.dismiss_modal_scene()
		
		
if __name__ == '__main__':
	scene_view = SceneView()
	scene_view.scene = FirstScene()
	second_scene = SecondScene()
	scene_view.present(hide_title_bar=True, animated=False)
	
# for use with https://github.com/omz/PythonistaAppTemplate

from scene import *
import ui

class FirstScene (Scene):
	def setup(self):
		self.background_color = 'midnightblue'
		self.ship = SpriteNode('spc:PlayerShip1Orange')
		self.ship.position = self.size / 2
		self.add_child(self.ship)
		
	def touch_began(self, touch):
		# question?
		# how do you get to the second scene?
		self.present_modal_scene(my_second_scene)
		
class SecondScene (Scene):
	def setup(self):
		self.background_color = '#704414'
		self.ship = SpriteNode('spc:EnemyGreen2')
		self.ship.position = self.size / 2
		self.add_child(self.ship)
		
	def touch_began(self, touch):
		pass
		
my_scene = FirstScene()
my_second_scene = SecondScene()
# Instead of...
# run(MyScene())

# ..use:
main_view = ui.View()
scene_view = SceneView(frame=main_view.bounds, flex='WH')
main_view.add_subview(scene_view)
scene_view.scene = my_scene
main_view.present(hide_title_bar=True, animated=False)

# --------------------

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
# --------------------

from scene import *


class FirstScene(Scene):
	def setup(self):
		# add white background
		SpriteNode(anchor_point=(0, 0), color='white', parent=self,
		size=self.size)
		self.ship = SpriteNode('spc:PlayerShip1Orange', parent=self,
		position=self.size / 2)
		
	def touch_began(self, touch):
		self.present_modal_scene(second_scene)
		
		
class SecondScene(Scene):
	def setup(self):
		# add green background
		SpriteNode(anchor_point=(0, 0), color='green', parent=self,
		size=self.size)
		self.ship = SpriteNode('spc:EnemyGreen2', parent=self,
		position=self.size / 2)
		
	def touch_began(self, touch):
		self.dismiss_modal_scene()
		
		
if __name__ == '__main__':
	scene_view = SceneView()
	scene_view.scene = FirstScene()
	second_scene = SecondScene()
	scene_view.present(hide_title_bar=True, animated=False)
# --------------------
# for use with https://github.com/omz/PythonistaAppTemplate

from scene import *
import ui
import time

class FirstScene (Scene):

	# global variable to class
	start_time = None
	
	def setup(self):
		# add background color
		self.background = SpriteNode(color = 'white')
		self.background.size = self.size
		self.background.position = self.size / 2
		self.add_child(self.background)
		
		# get starting time
		global start_time
		start_time = time.time()
		
		self.ship = SpriteNode('spc:PlayerShip1Orange')
		self.ship.position = self.size / 4
		self.add_child(self.ship)
		
	def update(self):
		# move to new scene after 1 second
		# problem is it keeps happening, since it is modal
		# is there a way to actually really dispose
		# of a scene and then move forward?
		
		current_time = time.time()
		if current_time - start_time > 1:
			#self.present_modal_scene(second_scene)
			pass
			
	def touch_began(self, touch):
		#self.dismiss_modal_scene()
		#self.present_modal_scene(second_scene)
		pass
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		if self.ship.frame.contains_point(touch.location):
			self.present_modal_scene(second_scene)
			
			
class SecondScene (Scene):

	# global variable to class
	start_time = None
	
	def setup(self):
		# add background color
		self.background = SpriteNode(color = 'green')
		self.background.size = self.size
		self.background.position = self.size / 2
		self.add_child(self.background)
		
		# get starting time
		global start_time
		start_time = time.time()
		
		self.ship = SpriteNode('spc:EnemyGreen2')
		self.ship.position = self.size / 2
		self.add_child(self.ship)
		
	def update(self):
		# move to new scene after 1 second
		current_time = time.time()
		if current_time - start_time > 1:
			#self.present_modal_scene(second_scene)
			pass
			
	def touch_began(self, touch):
	
		self.present_modal_scene(main_menu_scene)
		
		
class MainMenuScene (Scene):
	def setup(self):
		# add background color
		self.background = SpriteNode(color = 'blue')
		self.background.size = self.size
		self.background.position = self.size / 2
		self.add_child(self.background)
		
		self.ace = SpriteNode('card:ClubsA')
		self.ace.position = (683.0, 512.0)
		self.add_child(self.ace)
		
		self.king = SpriteNode('card:ClubsK')
		self.king.position = (683.0, 750.0)
		self.add_child(self.king)
		
		self.queen = SpriteNode('card:ClubsQ')
		self.queen.position = (683.0, 238.0)
		self.add_child(self.queen)
		
	def update(self):
		pass
		
	def touch_began(self, touch):
		#self.dismiss_modal_scene()
		#self.present_modal_scene(a_scene)
		pass
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		# move to new scenes
		if self.ace.frame.contains_point(touch.location):
			self.present_modal_scene(a_scene)
		elif self.king.frame.contains_point(touch.location):
			self.present_modal_scene(b_scene)
		elif self.queen.frame.contains_point(touch.location):
			self.present_modal_scene(c_scene)
			
			
class AScene (Scene):
	def setup(self):
		# add background color
		self.background = SpriteNode(color = 'white')
		self.background.size = self.size
		self.background.position = self.size / 2
		self.add_child(self.background)
		
		self.a_choise = SpriteNode('card:BackBlue1')
		self.a_choise.position = self.size / 2
		self.add_child(self.a_choise)
		
	def update(self):
		pass
		
	def touch_began(self, touch):
		self.dismiss_modal_scene()
		#self.present_modal_scene(b_scene)
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		pass
		
		
class BScene (Scene):
	def setup(self):
		# add background color
		self.background = SpriteNode(color = 'white')
		self.background.size = self.size
		self.background.position = self.size / 2
		self.add_child(self.background)
		
		self.ship = SpriteNode('card:BackGreen1')
		self.ship.position = self.size / 2
		self.add_child(self.ship)
		
	def update(self):
		pass
		
	def touch_began(self, touch):
		self.dismiss_modal_scene()
		#self.present_modal_scene(c_scene)
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		pass
		
		
class CScene (Scene):
	def setup(self):
		# add background color
		self.background = SpriteNode(color = 'white')
		self.background.size = self.size
		self.background.position = self.size / 2
		self.add_child(self.background)
		
		self.ship = SpriteNode('card:BackRed1')
		self.ship.position = self.size / 2
		self.add_child(self.ship)
		
	def update(self):
		pass
		
	def touch_began(self, touch):
		self.dismiss_modal_scene()
		#self.present_modal_scene(second_scene)
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		pass
		
		
first_scene = FirstScene()
second_scene = SecondScene()
main_menu_scene = MainMenuScene()
a_scene = AScene()
b_scene = BScene()
c_scene = CScene()
# Instead of...
# run(MyScene())

# ..use:
main_view = ui.View()
scene_view = SceneView(frame=main_view.bounds, flex='WH')
main_view.add_subview(scene_view)
scene_view.scene = first_scene
main_view.present(hide_title_bar=True, animated=False)
# --------------------
# for use with https://github.com/omz/PythonistaAppTemplate

from scene import *
import ui
import time

class FirstScene (Scene):

	# global variable to class
	start_time = None
	
	def setup(self):
		# add background color
		self.background = SpriteNode(color = 'white')
		self.background.size = self.size
		self.background.position = self.size / 2
		self.add_child(self.background)
		
		# get starting time
		global start_time
		start_time = time.time()
		
		self.ship = SpriteNode('test:Pythonista')
		self.ship.position = self.size / 2
		self.ship.size = self.size
		self.add_child(self.ship)
		
	def update(self):
		# move to new scene after 2 second
		# problem is it keeps happening, since it is modal
		# is there a way to actually really dispose
		# of a scene and then move forward?
		
		current_time = time.time()
		
		#global scene_moved_away_from
		if current_time - start_time > 2:
			self.present_modal_scene(second_scene)
			
	def touch_began(self, touch):
		#self.present_modal_scene(second_scene)
		pass
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		if self.ship.frame.contains_point(touch.location):
			self.present_modal_scene(second_scene)
			
			
class SecondScene (Scene):

	# global variable to class
	start_time = None
	
	def setup(self):
		# add background color
		self.background = SpriteNode(color = 'green')
		self.background.size = self.size
		self.background.position = self.size / 2
		self.add_child(self.background)
		
		start_time = time.time()
		
		self.ship = SpriteNode('spc:EnemyGreen2')
		self.ship.position = self.size / 2
		self.add_child(self.ship)
		
	def update(self):
		# move to new scene after 2 second
		current_time = time.time()
		
		# have to comment out because get "max recursion error"
		# code keeps reloading first then second scene over and
		# over again, since time has lapsed
		#if current_time - start_time > 2:
			#self.present_modal_scene(second_scene)
			#pass
			
	def touch_began(self, touch):
		self.pause = True
		self.present_modal_scene(main_menu_scene)
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		pass
		
		
class MainMenuScene (Scene):

	def setup(self):
		# add background color
		self.background = SpriteNode(color = 'blue')
		self.background.size = self.size
		self.background.position = self.size / 2
		self.add_child(self.background)
		
		self.ace = SpriteNode('card:ClubsA')
		self.ace.position = (683.0, 512.0)
		self.add_child(self.ace)
		
		self.king = SpriteNode('card:ClubsK')
		self.king.position = (683.0, 750.0)
		self.add_child(self.king)
		
		self.queen = SpriteNode('card:ClubsQ')
		self.queen.position = (683.0, 238.0)
		self.add_child(self.queen)
		
	def update(self):
		pass
		
	def touch_began(self, touch):
		pass
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		# move to new scenes
		if self.ace.frame.contains_point(touch.location):
			self.present_modal_scene(a_scene)
		elif self.king.frame.contains_point(touch.location):
			self.present_modal_scene(b_scene)
		elif self.queen.frame.contains_point(touch.location):
			self.present_modal_scene(c_scene)
			
			
class AScene (Scene):

	def setup(self):
		# add background color
		self.background = SpriteNode(color = 'white')
		self.background.size = self.size
		self.background.position = self.size / 2
		self.add_child(self.background)
		
		self.blue_card = SpriteNode('card:BackBlue1')
		self.blue_card.position = self.size / 2
		self.add_child(self.blue_card)
		
	def update(self):
		pass
		
	def touch_began(self, touch):
		pass
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		# moving back to previous scene, so remove modal makes sense
		if self.blue_card.frame.contains_point(touch.location):
			self.dismiss_modal_scene()
			
			
class BScene (Scene):

	def setup(self):
		# add background color
		self.background = SpriteNode(color = 'white')
		self.background.size = self.size
		self.background.position = self.size / 2
		self.add_child(self.background)
		
		self.green_card = SpriteNode('card:BackGreen1')
		self.green_card.position = self.size / 2
		self.add_child(self.green_card)
		
	def update(self):
		pass
		
	def touch_began(self, touch):
		pass
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		# moving back to previous scene, so remove modal makes sense
		if self.green_card.frame.contains_point(touch.location):
			self.dismiss_modal_scene()
			
			
class CScene (Scene):

	def setup(self):
		# add background color
		self.background = SpriteNode(color = 'white')
		self.background.size = self.size
		self.background.position = self.size / 2
		self.add_child(self.background)
		
		self.red_card = SpriteNode('card:BackRed1')
		self.red_card.position = self.size / 2
		self.add_child(self.red_card)
		
	def update(self):
		pass
		
	def touch_began(self, touch):
		pass
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		# moving back to previous scene, so remove modal makes sense
		if self.red_card.frame.contains_point(touch.location):
			self.dismiss_modal_scene()
			
			
first_scene = FirstScene()
second_scene = SecondScene()
main_menu_scene = MainMenuScene()
a_scene = AScene()
b_scene = BScene()
c_scene = CScene()
# Instead of...
# run(MyScene())

# ..use:
main_view = ui.View()
scene_view = SceneView(frame=main_view.bounds, flex='WH')
main_view.add_subview(scene_view)
scene_view.scene = first_scene
main_view.present(hide_title_bar=True, animated=False)
# --------------------

