# Card Game
#
# In this game, you have to find matching pairs of cards.
# This scene consists entirely of layers and demonstrates some
# interesting animation techniques.

from scene import *
from random import shuffle
from functools import partial
import sound

class Game (Scene):
	def setup(self):
		self.root_layer = Layer(self.bounds)
		for effect in ['Click_1', 'Click_2', 'Coin_2', 'Coin_5']:
			sound.load_effect(effect)
		
		self.deal()
	
	def draw(self):
		background(0.0, 0.2, 0.3)
		self.root_layer.update(self.dt)
		self.root_layer.draw()
	
	def deal(self):
		images = ['Rabbit_Face', 'Mouse_Face', 'Cat_Face',
		          'Dog_Face', 'Octopus', 'Bear_Face',
		          'Chicken', 'Cow_Face'] * 2
		for image in images:
			load_image(image)
		shuffle(images)
		self.root_layer.sublayers = []
		self.cards = []
		self.selected = []
		card_size = 96 if self.size.w > 700 else 64
		width = (card_size + 5) * 4
		offset = Point((self.size.w - width)/2,
		               (self.size.h - width)/2)
		for i in xrange(len(images)):
			x, y = i % 4, i / 4
			card = Layer(Rect(offset.x + x * (card_size + 5),
			                  offset.y + y * (card_size + 5),
			                  card_size, card_size))
			card.card_image = images[i]
			card.background = Color(0.9, 0.9, 0.9)
			card.stroke = Color(1, 1, 1)
			card.stroke_weight = 4.0
			self.add_layer(card)
			self.cards.append(card)
		self.touch_disabled = False
	
	def touch_began(self, touch):
		if self.touch_disabled or len(self.cards) == 0:
			return
		if len(self.selected) == 2:
			self.discard_selection()
			return
		for card in self.cards:
			if card in self.selected or len(self.selected) > 1:
				continue
			if touch.location in card.frame:
				def reveal_card():
					card.image = card.card_image
					card.animate('scale_x', 1.0, 0.15,
					             completion=self.check_selection)
				self.selected.append(card)
				self.touch_disabled = True
				card.animate('scale_x', 0.0, 0.15,
				             completion=reveal_card)
				card.scale_y = 1.0
				card.animate('scale_y', 0.9, 0.15, autoreverse=True)
				sound.play_effect('Click_1')
				break
	
	def discard_selection(self):
		sound.play_effect('Click_2')
		for card in self.selected:
			def conceal(card):
				card.image = None
				card.animate('scale_x', 1.0, 0.15)
			card.animate('scale_x', 0.0, 0.15,
			             completion=partial(conceal, card))
			card.scale_y = 1.0
			card.animate('scale_y', 0.9, 0.15, autoreverse=True)
		self.selected = []
	
	def check_selection(self):
		self.touch_disabled = False
		if len(self.selected) == 2:
			card_img1 = self.selected[0].card_image
			card_img2 = self.selected[1].card_image
			if card_img1 == card_img2:
				sound.play_effect('Coin_5')
				for c in self.selected:
					c.animate('background', Color(0.5, 1, 0.5))
					self.cards.remove(c)
					self.selected = []
					if len(self.cards) == 0:
						self.win()
	
	def new_game(self):
		sound.play_effect('Coin_2')
		self.deal()
		self.root_layer.animate('scale_x', 1.0)
		self.root_layer.animate('scale_y', 1.0)
	
	def win(self):
		self.delay(0.5, partial(sound.play_effect, 'Powerup_2'))
		font_size = 100 if self.size.w > 700 else 50
		text_layer = TextLayer('Well Done!', 'Futura', font_size)
		text_layer.frame.center(self.bounds.center())
		overlay = Layer(self.bounds)
		overlay.background = Color(0, 0, 0, 0)
		overlay.add_layer(text_layer)
		self.add_layer(overlay)
		overlay.animate('background', Color(0.0, 0.2, 0.3, 0.7))
		text_layer.animate('scale_x', 1.3, 0.3, autoreverse=True)
		text_layer.animate('scale_y', 1.3, 0.3, autoreverse=True)
		self.touch_disabled = True
		self.root_layer.animate('scale_x', 0.0, delay=2.0,
								curve=curve_ease_back_in)
		self.root_layer.animate('scale_y', 0.0, delay=2.0,
								curve=curve_ease_back_in,
								completion=self.new_game)
run(Game())
