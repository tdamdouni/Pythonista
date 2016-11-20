# https://gist.github.com/anonymous/cb0ac079b7351e2b59e980237a546152

# https://forum.omz-software.com/topic/3591/removing-missile-when-goes-off-screen

# Created by: Mr. Coxall
# Created on: Sep 2016
# Created for: ICS3U
# This program is the first file in a multi-scene game template
#    This template is meant to be used with the Xcode

from scene import *
import ui
from numpy import random
from copy import deepcopy

class FirstScene(Scene):
	def setup(self):
		# this method is called, when user moves to this scene
		
		self.size_of_screen = deepcopy(self.size)
		self.center_of_screen = deepcopy(self.size/2)
		self.left_button_down = False
		self.right_button_down = False
		self.ship_move_speed = 40.0
		self.missiles = []
		self.aliens = []
		self.alien_attack_rate = 1
		self.alien_attack_speed = 20.0
		
		# add blue background color
		self.background = SpriteNode(position = self.size / 2,
		color = (0.61, 0.78, 0.87),
		parent = self,
		size = self.size)
		
		spaceship_position = deepcopy(self.center_of_screen)
		spaceship_position.y = 100
		self.spaceship = SpriteNode('spc:PlayerShip1Orange',
		parent = self,
		position = spaceship_position)
		
		left_button_position = deepcopy(self.center_of_screen)
		left_button_position.x = 75
		left_button_position.y = 75
		self.left_button = SpriteNode('iob:arrow_left_a_256',
		parent = self,
		scale = 0.5,
		position = left_button_position,
		alpha = 0.5)
		
		right_button_position = deepcopy(self.center_of_screen)
		right_button_position.x = 200
		right_button_position.y = 75
		self.right_button = SpriteNode('iob:arrow_right_a_256',
		parent = self,
		scale = 0.5,
		position = right_button_position,
		alpha = 0.5)
		
		fire_button_position = deepcopy(self.size)
		fire_button_position.x = fire_button_position.x - 75
		fire_button_position.y = 75
		self.fire_button = SpriteNode('iob:disc_256',
		parent = self,
		scale = 0.5,
		position = fire_button_position,
		alpha = 0.5)
		
	def update(self):
		# this method is called, hopefully, 60 times a second
		
		# move spaceship if button down
		if self.left_button_down == True:
			spaceshipMove = Action.move_by(-1*self.ship_move_speed,
			0.0,
			0.1)
			self.spaceship.run_action(spaceshipMove)
		if self.right_button_down == True:
			spaceshipMove = Action.move_by(self.ship_move_speed,
			0.0,
			0.1)
			self.spaceship.run_action(spaceshipMove)
			
		# check every update if a missile is off screen
		print('A: ' + str(range(len(self.missiles))))
		for i, missile in enumerate(self.missiles):
			print(i, missile.position)
			if missile.position.y > self.size_of_screen.y - 100:
				missile.remove_from_parent()
			self.missiles.remove(missile)
		#for missile_index in range(len(self.missiles)):
		
			#if self.missiles[missile_index].position.y > self.size_of_screen.y - 100:
								#self.missiles[missile_index].remove_all_actions()
								#self.missiles[missile_index].remove_from_parent()
								#print('B: ' + str(missile_index) + ' ' + str(len(self.missiles)))
								#print(missile_index)
								#self.missiles.remove(missile_index)
								#print('one success')
								#break
								#print(len(self.missiles))
								
	def touch_began(self, touch):
		# this method is called, when user touches the screen
		
		# check if left or right button is down
		if self.left_button.frame.contains_point(touch.location):
			self.left_button_down = True
			
		if self.right_button.frame.contains_point(touch.location):
			self.right_button_down = True
			
	def touch_moved(self, touch):
		# this method is called, when user moves a finger around on the screen
		pass
		
	def touch_ended(self, touch):
		# this method is called, when user releases a finger from the screen
		
		# if I removed my finger, then no matter what spaceship
		#    should not be moving any more
		self.left_button_down = False
		self.right_button_down = False
		
		# if fire button pressed, create a new missile
		if self.fire_button.frame.contains_point(touch.location):
			self.create_new_missile()
			
	def create_new_missile(self):
		# when the user hits the fire button
		
		missile_start_position = deepcopy(self.spaceship.position)
		missile_start_position.y = 100
		
		missile_end_position = deepcopy(self.size)
		missile_end_position.x = missile_start_position.x
		
		self.missiles.append(SpriteNode('spc:Fire1',
		position = missile_start_position,
		parent = self))
		
		# make missile move forward
		missileMoveAction = Action.move_to(missile_end_position.x,
		missile_end_position.y + 100,
		1.0)
		self.missiles[len(self.missiles)-1].run_action(missileMoveAction)
		
		
#  ..use when deploying app for Xcode and the App Store
main_view = ui.View()
scene_view = SceneView(frame = main_view.bounds, flex = 'WH')
main_view.add_subview(scene_view)
scene_view.scene = FirstScene()
main_view.present(hide_title_bar = True, animated = False)

