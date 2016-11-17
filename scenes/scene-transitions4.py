# for use with https://github.com/omz/PythonistaAppTemplate

from scene import *
import time


class FirstScene(Scene):
	def setup(self):
		# get starting time
		self.start_time = time.time()
		# add background color
		SpriteNode(anchor_point=(0, 0), color='white', parent=self,
		size=self.size)
		self.ship = SpriteNode('test:Pythonista', anchor_point=(0, 0),
		parent=self, size=self.size)
		
	def update(self):
		# move to new scene after 2 seconds
		if not self.presented_scene and time.time() - self.start_time > 2:
			self.present_modal_scene(SecondScene())
			
	def touch_began(self, touch):
		# self.present_modal_scene(SecondScene())
		pass
		
	def touch_ended(self, touch):
		if self.ship.frame.contains_point(touch.location):
			self.present_modal_scene(SecondScene())
			
			
class SecondScene(Scene):
	def setup(self):
		self.start_time = time.time()
		# add background color
		SpriteNode(anchor_point=(0, 0), color='green', parent=self,
		size=self.size)
		self.ship = SpriteNode('spc:EnemyGreen2', parent=self,
		position=self.size/2)
		
	def update(self):
		if not self.presented_scene and time.time() - self.start_time > 2:
			self.present_modal_scene(MainMenuScene())
			
	def touch_began(self, touch):
		self.present_modal_scene(MainMenuScene())
		
		
class MainMenuScene (Scene):
	def setup(self):
		# add background color
		SpriteNode(anchor_point=(0, 0), color='blue', parent=self,
		size=self.size)
		
		self.ace = SpriteNode('card:ClubsA', parent=self, position=(683, 512))
		self.king = SpriteNode('card:ClubsK', parent=self, position=(683, 750))
		self.queen = SpriteNode('card:ClubsQ', parent=self, position=(683, 238))
		
	def touch_ended(self, touch):
		# move to new scenes
		if self.ace.frame.contains_point(touch.location):
			self.present_modal_scene(CardBackScene('blue'))
		elif self.king.frame.contains_point(touch.location):
			self.present_modal_scene(CardBackScene('green'))
		elif self.queen.frame.contains_point(touch.location):
			self.present_modal_scene(CardBackScene('red'))
			
			
class CardBackScene(Scene):
	def __init__(self, card_back_color='blue'):
		Scene.__init__(self)
		self.img_name = 'card:Back{}1'.format(card_back_color.title())
		
	def setup(self):
		# add background color
		SpriteNode(anchor_point=(0, 0), color='white', parent=self,
		size=self.size)
		self.card = SpriteNode(self.img_name, parent=self,
		position=self.size/2)
		
	def touch_ended(self, touch):
		# moving back to previous scene, so remove modal makes sense
		if self.card.frame.contains_point(touch.location):
			self.dismiss_modal_scene()
			
			
main_view = SceneView()
main_view.scene = FirstScene()
main_view.present(hide_title_bar=True, animated=False)

