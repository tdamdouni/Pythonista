# coding: utf-8

# https://gist.github.com/offe/95d9189cc62bb9d268e7

from scene import *
import sound
import random
import math
A = Action

class MainMenuScene(Scene):
	def __init__(self):
		self._high_score = 0
		Scene.__init__(self)
	
	@property
	def high_score(self):
		return self._high_score
		
	@high_score.setter
	def high_score(self, high_score):
		self._high_score = high_score
		if self.score_node.children:
			self.score_node.children[0].remove_from_parent()
		LabelNode('High Score: %d' % self._high_score, position=(self.size * (0.5, 0.8)), 
							font=('Helvetica', self.size[1]*0.08), parent=self.score_node)
	
	def setup(self):
		self.background_color = 'midnightblue'
		LabelNode('The Game', position=(self.size * (0.5, 0.9)), 
							font=('Helvetica', self.size[1]*0.1), parent=self)
		self.play_node = SpriteNode('iow:play_256', 
																position=self.size*(0.5, 0.5),
																scale=self.size[1]/768.0*1.0, 
																parent=self)
		self.settings_node = SpriteNode('iow:ios7_gear_256', 
																position=self.size*(0.3, 0.2), 
																scale=self.size[1]/768.0*0.8, 
																parent=self)
		self.credits_node = SpriteNode('iow:information_circled_256', 
																position=self.size*(0.7, 0.2), 
																scale=self.size[1]/768.0*0.7, 
																parent=self)
		self.score_node = Node(parent=self)
		self.high_score = self._high_score

	def touch_ended(self, touch):
		next_scene = None
		if self.play_node.frame.contains_point(touch.location):
			next_scene = PlayScene(self)
		elif self.settings_node.frame.contains_point(touch.location):
			next_scene = SettingsScene(self)
		elif self.credits_node.frame.contains_point(touch.location):
			next_scene = CreditsScene(self)
		if next_scene:
			next_scene.setup()
			self.scene_switcher.switch_scene(next_scene)

class CreditsScene (Scene):
	def __init__(self, previous_scene):
		self.previous_scene = previous_scene
		Scene.__init__(self)
	
	def setup(self):
		LabelNode('Credits', position=(self.size * (0.5, 0.9)), 
							font=('Helvetica', self.size[1]/20), parent=self)
		self.back_node = SpriteNode('iow:ios7_undo_256', scale=self.size[1]/768.0*.6, 
																position=self.size*(0.1, 0.9), parent=self)
	
	def touch_ended(self, touch):
		if self.back_node.frame.contains_point(touch.location):
			self.scene_switcher.switch_scene(self.previous_scene)

class SettingsScene (Scene):
	def __init__(self, previous_scene):
		self.previous_scene = previous_scene
		Scene.__init__(self)
		
	def setup(self):
		LabelNode('Settings', position=(self.size * (0.5, 0.9)), 
							font=('Helvetica', self.size[1]/20), parent=self)
		self.back_node = SpriteNode('iow:ios7_undo_256', scale=self.size[1]/768.0*.6, 
																position=self.size*(0.1, 0.9), parent=self)
	
	def touch_ended(self, touch):
		if self.back_node.frame.contains_point(touch.location):
			self.scene_switcher.switch_scene(self.previous_scene)

class PlayScene(Scene):
	def __init__(self, main_menu):
		self.main_menu = main_menu
		self.score = 0
		Scene.__init__(self)
		
	def setup(self):
		self.up_node = LabelNode('+1', position=(self.size * (0.25, 0.5)), 
																font=('Helvetica', self.size[1]*0.3), parent=self)
		self.game_over_node = LabelNode('Game Over', 
																		position=(self.size * (0.75, 0.5)), 
																		font=('Helvetica', self.size[1]*0.08), parent=self)
		self.score_node = Node(parent=self)
		self.update_score()

	def update_score(self):
		if self.score_node.children:
			self.score_node.children[0].remove_from_parent()
		LabelNode(str(self.score), 
							position=(self.size * (0.05, 0.95)), 
																font=('Helvetica', self.size[1]*0.08), parent=self.score_node)

	def touch_ended(self, touch):
		if self.up_node.frame.contains_point(touch.location):
			self.score += 1
			self.update_score()
		elif self.game_over_node.frame.contains_point(touch.location):
			if self.score > self.main_menu.high_score:
				self.main_menu.high_score = self.score
				next_scene = NewHighScoreScene(self.score, self.main_menu)
				next_scene.setup()
				self.scene_switcher.switch_scene(next_scene)
			else:
				self.scene_switcher.switch_scene(self.main_menu)


class NewHighScoreScene (Scene):
	def __init__(self, score, main_menu):
		self.score = score
		self.main_menu = main_menu
		Scene.__init__(self)
		
	def setup(self):
		self.background_color = 'black'
		LabelNode('New High Score!', position=(self.size[0]/2, self.size[1]*0.9), 
							font=('Helvetica', self.size[0]/20), parent=self)
		LabelNode(str(self.score), position=(self.size[0]/2, self.size[1]*0.4), 
							font=('Helvetica', self.size[1]/2), parent=self)

	def touch_ended(self, touch):
		self.scene_switcher.switch_scene(self.main_menu)

class SceneSwitcher (Scene):
	def __init__(self, start_scene):
		start_scene.scene_switcher = self
		self.active_scene = start_scene
		Scene.__init__(self)

	def switch_scene(self, new_scene):
		new_scene.scene_switcher = self
		for node in self.children:
			node.remove_from_parent()
			self.active_scene.add_child(node)
		self.active_scene = new_scene
		self.setup()
		
	def setup(self):
		self.background_color = self.active_scene.background_color
		for node in self.active_scene.children:
			node.remove_from_parent()
			self.add_child(node)
			
	def did_change_size(self):
		self.active_scene.size = self.size
		self.active_scene.did_change_size()

	def touch_began(self, touch):
		self.active_scene.touch_began(touch)

	def touch_moved(self, touch):
		self.active_scene.touch_moved(touch)
		
	def touch_ended(self, touch):
		self.active_scene.touch_ended(touch)

if __name__ == '__main__':
	main_menu = MainMenuScene()
	main_menu.setup()
	
	scene_switcher = SceneSwitcher(main_menu)
	run(scene_switcher, orientation=LANDSCAPE, show_fps=False)
	
	#run(main_menu)
	#run(CreditsScene(main_menu), orientation=LANDSCAPE, show_fps=False)
	#run(SettingsScene(main_menu), orientation=LANDSCAPE, show_fps=False)
	#run(PlayScene(), orientation=LANDSCAPE, show_fps=False)
	#run(NewHighScoreScene(12), orientation=LANDSCAPE, show_fps=False)