# coding: utf-8

# https://gist.github.com/offe/a58d34573d8f5c89743a

from scene import *
import sound
import random
import math
A = Action

class TransitionImmediate (object):
	def run(self, scene_switcher, new_scene):
		scene_switcher.active_scene.remove_from_parent()
		scene_switcher.active_scene = new_scene
		scene_switcher.show_active_scene()


class TransitionCrossFade (object):
	def __init__(self, duration=1.0, timing=TIMING_EASE_IN_OUT):
		self.duration = duration
		self.timing = timing
		
	def run(self, scene_switcher, new_scene):
		old_scene = scene_switcher.active_scene
		scene_switcher.active_scene = new_scene
		old_scene.run_action(A.sequence(
			A.fade_to(0.0, self.duration, self.timing), 
			A.remove()
		))
		scene_switcher.behindall.color = old_scene.background_color
		scene_switcher.behindall.alpha = 1.0
		scene_switcher.show_active_scene()
		scene_switcher.active_scene.alpha = 0.0
		scene_switcher.active_scene.run_action(A.fade_to(1.0, self.duration, self.timing))
		scene_switcher.behindall.run_action(A.fade_to(0.0, self.duration, self.timing))


class TransitionFadeWithColor (object):
	def __init__(self, color='black', duration=1.0, timing=TIMING_EASE_IN_OUT):
		self.color = color
		self.duration = duration
		self.timing = timing
		
	def run(self, scene_switcher, new_scene):
		old_scene = scene_switcher.active_scene
		scene_switcher.active_scene = new_scene
		scene_switcher.coverall.color = self.color
		old_scene.run_action(A.sequence(A.wait(self.duration/2), A.remove()))
		scene_switcher.coverall.run_action(A.sequence(
			A.fade_to(1.0, self.duration/2, self.timing), 
			A.fade_to(0.0, self.duration/2, self.timing)
		))
		scene_switcher.run_action(A.sequence(
			A.wait(self.duration/2), 
			A.call(scene_switcher.show_active_scene)
		))
	

class TransitionPush (object):
	def __init__(self, direction=None, duration=1.0, timing=TIMING_EASE_IN_OUT):
		self.direction = direction
		self.duration = duration
		self.timing = timing
		
	def run(self, scene_switcher, new_scene):
		if self.direction is None:
			self.direction = scene_switcher.size * (1.0, 0.0)
		x, y = self.direction
		old_scene = scene_switcher.active_scene
		scene_switcher.active_scene = new_scene
		old_scene.run_action(A.sequence(
			A.move_by(-x, -y, self.duration, self.timing), 
			A.move_by(x, y, 0.0), 
			A.remove()
		))
		scene_switcher.behindall.color = old_scene.background_color
		scene_switcher.behindall.alpha = 1.0
		scene_switcher.active_scene.position += self.direction
		scene_switcher.show_active_scene()
		scene_switcher.active_scene.run_action(A.move_by(-x, -y, self.duration, self.timing))
		scene_switcher.behindall.run_action(A.fade_to(0.0, self.duration, self.timing))
		

class SceneSwitcher (Scene):
	def __init__(self, start_scene):
		start_scene.scene_switcher = self
		self.active_scene = start_scene
		Scene.__init__(self)

	def present(self, new_scene, transition=None):
		new_scene.scene_switcher = self
		if transition is None:
			transition = TransitionImmediate()
		transition.run(self, new_scene)
		
	def setup(self):
		self.behindall = SpriteNode(position=self.size/2, size=self.size, parent=self, alpha=0.0)
		self.scene_node = Node(parent=self)
		self.coverall = SpriteNode(position=self.size/2, size=self.size, parent=self, alpha=0.0, color='black')
		self.show_active_scene()
		
	def show_active_scene(self):
		self.background_color = self.active_scene.background_color
		self.scene_node.add_child(self.active_scene)
			
	def did_change_size(self):
		self.active_scene.size = self.size
		self.active_scene.did_change_size()

	def update(self):
		self.active_scene.dt = self.dt
		self.active_scene.t = self.t
		self.active_scene.update()

	def touch_began(self, touch):
		self.active_scene.touch_began(touch)

	def touch_moved(self, touch):
		self.active_scene.touch_moved(touch)
		
	def touch_ended(self, touch):
		self.active_scene.touch_ended(touch)


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
		self.score_node.text = 'High Score: %d' % self._high_score
	
	def setup(self):
		self.background_color = 'midnightblue'
		self.title_node = LabelNode('The Game', position=(self.size * (0.5, 0.9)), 
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
		self.score_node = LabelNode('High Score: %d' % self._high_score, position=(self.size * (0.5, 0.8)), 
																font=('Helvetica', self.size[1]*0.08), parent=self)
		self.high_score = self._high_score

	def update(self):
		self.title_node.position = self.size * (0.5 + 0.1*math.sin(self.t), 
																						0.9 + 0.01*math.sin(2.83*self.t+1.0))

	def touch_ended(self, touch):
		next_scene = None
		if self.play_node.frame.contains_point(touch.location):
			play_scene = PlayScene(self)
			play_scene.setup()
			self.scene_switcher.present(play_scene, TransitionFadeWithColor('black', duration=0.5))
		elif self.settings_node.frame.contains_point(touch.location):
			next_scene = SettingsScene(self)
		elif self.credits_node.frame.contains_point(touch.location):
			next_scene = CreditsScene(self)
		if next_scene:
			next_scene.setup()
			self.scene_switcher.present(next_scene, TransitionPush(self.size * (1.0, 0.0), duration=0.5))


class CreditsScene (Scene):
	def __init__(self, previous_scene):
		self.previous_scene = previous_scene
		Scene.__init__(self)
	
	def setup(self):
		self.background_color = 'lightgrey'
		LabelNode('Credits', position=(self.size * (0.5, 0.9)), 
							font=('Helvetica', self.size[1]/20), parent=self)
		self.back_node = SpriteNode('iow:ios7_undo_256', scale=self.size[1]/768.0*.6, 
																position=self.size*(0.1, 0.9), parent=self)
	
	def touch_ended(self, touch):
		if self.back_node.frame.contains_point(touch.location):
			self.scene_switcher.present(self.previous_scene, 
																	TransitionPush(self.size * (-1.0, 0.0), duration=0.5))


class SettingsScene (Scene):
	def __init__(self, previous_scene):
		self.previous_scene = previous_scene
		Scene.__init__(self)
		
	def setup(self):
		self.background_color = 'lightgrey'
		LabelNode('Settings', position=(self.size * (0.5, 0.9)), 
							font=('Helvetica', self.size[1]/20), parent=self)
		self.back_node = SpriteNode('iow:ios7_undo_256', scale=self.size[1]/768.0*.6, 
																position=self.size*(0.1, 0.9), parent=self)
	
	def touch_ended(self, touch):
		if self.back_node.frame.contains_point(touch.location):
			self.scene_switcher.present(self.previous_scene, 
																	TransitionPush(self.size * (-1.0, 0.0), duration=0.5))


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
		self.score_node = LabelNode(str(self.score), 
																position=(self.size * (0.05, 0.95)), 
																font=('Helvetica', self.size[1]*0.08), parent=self)

	def update_score(self):
		self.score_node.text = str(self.score)

	def touch_ended(self, touch):
		if self.up_node.frame.contains_point(touch.location):
			self.score += 1
			self.update_score()
		elif self.game_over_node.frame.contains_point(touch.location):
			if self.score > self.main_menu.high_score:
				self.main_menu.high_score = self.score
				next_scene = NewHighScoreScene(self.score, self.main_menu)
				next_scene.setup()
				self.scene_switcher.present(next_scene, TransitionFadeWithColor('white', duration=1.0))
			else:
				self.scene_switcher.present(self.main_menu, TransitionFadeWithColor('black', duration=0.5))


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
		self.scene_switcher.present(self.main_menu, TransitionCrossFade())


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