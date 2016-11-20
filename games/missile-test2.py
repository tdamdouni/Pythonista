# https://forum.omz-software.com/topic/3591/removing-missile-when-goes-off-screen/5

# Created by: Mr. Coxall
# Created on: Sep 2016
# Created for: ICS3U
# This program is the first file in a multi-scene game template
#    This template is meant to be used with the Xcode

import scene
import ui
Action = scene.Action


class FirstScene(scene.Scene):
	def setup(self):
		# this method is called, when user moves to this scene
		self.left_button_down = False
		self.right_button_down = False
		self.ship_move_speed = 40.0
		self.missiles = []
		# self.aliens = []
		# self.alien_attack_rate = 1
		# self.alien_attack_speed = 20.0
		
		# add blue background color
		scene.SpriteNode(position=self.size / 2,
		color=(0.61, 0.78, 0.87),
		parent=self,
		size=self.size)
		
		position = scene.Point(self.size.x / 2, 100)
		self.spaceship = scene.SpriteNode('spc:PlayerShip1Orange',
		parent=self,
		position=position)
		
		self.left_button = scene.SpriteNode('iob:arrow_left_a_256',
		parent=self,
		scale=0.5,
		position=scene.Point(75, 75),
		alpha=0.5)
		
		self.right_button = scene.SpriteNode('iob:arrow_right_a_256',
		parent=self,
		scale=0.5,
		position=scene.Point(200, 75),
		alpha=0.5)
		
		position = scene.Point(self.size.x - 75, 75)
		self.fire_button = scene.SpriteNode('iob:disc_256',
		parent=self,
		scale=0.5,
		position=position,
		alpha=0.5)
		
	def update(self):
		# this method is called, hopefully, 60 times a second
		# move spaceship if button down
		if self.left_button_down:
			self.spaceship.run_action(Action.move_by(-self.ship_move_speed,
			0.0,
			0.1))
		if self.right_button_down:
			self.spaceship.run_action(Action.move_by(self.ship_move_speed,
			0.0,
			0.1))
			
		# check every update if a missile is off screen
		print('A: {}'.format(len(self.missiles)))
		for i, missile in enumerate(self.missiles):
			print(i, missile.position)
			if missile.position.y > self.size.y - 100:
				missile.remove_from_parent()
				self.missiles.remove(missile)
				break
				
	def touch_began(self, touch):
		# this method is called, when user touches the screen
		
		# check if left or right button is down
		self.left_button_down = touch.location in self.left_button.frame
		self.right_button_down = touch.location in self.right_button.frame
		
	def touch_moved(self, touch):
		# this method is called, when user moves a finger around on the screen
		pass
		
	def touch_ended(self, touch):
		# this method is called, when user releases a finger from the screen
		
		# if I removed my finger,
		# then no matter what spaceship should not be moving any more
		self.left_button_down = False
		self.right_button_down = False
		
		# if fire button pressed, create a new missile
		if touch.location in self.fire_button.frame:
			self.create_new_missile()
			
	def create_new_missile(self):
		# when the user hits the fire button
		missle = scene.SpriteNode('spc:Fire1',
		position=self.spaceship.position,
		parent=self)
		missle.run_action(Action.move_to(self.spaceship.position.x,
		self.size.y + 100,
		1.0))
		self.missiles.append(missle)
		
		
#  ..use when deploying app for Xcode and the App Store
if __name__ == '__main__':
	main_view = ui.View()
	scene_view = scene.SceneView(frame=main_view.bounds, flex='WH')
	scene_view.scene = FirstScene()
	main_view.add_subview(scene_view)
	main_view.present(hide_title_bar=True, animated=False)
	
	# scene_view = scene.SceneView()
	# scene_view.scene = FirstScene()
	# scene_view.present(hide_title_bar = True, animated = False)
	
	# scene.run(FirstScene())

