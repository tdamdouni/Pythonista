# https://gist.github.com/git-bee/f7253920814c7db7176a

# Memory Card Game
#
# In this game, you have to find matching pairs of cards.
# This scene consists entirely of layers and demonstrates some
# interesting animation techniques.
#
# Originally sample of Pythonista app.
# Modified and enhanced by @beezing.
# Added more image theme and simple scoring.

import speech
from scene import *
from random import shuffle, sample, randint
from functools import partial
import sound

def ngomong(txt):
	speech.say(txt,'id',0.25)
	
class Game (Scene):
	def setup(self):
		self.root_layer = Layer(self.bounds)
		for effect in ['Click_1', 'Click_2', 'Coin_2', 'Coin_5']:
			sound.load_effect(effect)
		self.deal()
		
	def should_rotate(self, orientation):
		return False
		
	def draw(self):
		background(0.0, 0.2, 0.3)
		self.root_layer.update(self.dt)
		self.root_layer.draw()
		
		# draw title and score
		title = 'Kartu Ingatan' # 'Memory Cards'
		if not self.size.w > 320:
			text(title, 'Arial', 24, self.size.w/2, self.size.h-50)
		else:
			for i in xrange(len(title)):
				text(title[i], 'Arial', 24, 50, self.size.h - i*20 - 40)
		if not self.size.w > 320:
			text(str(self.tap_count), 'Arial', 20, self.size.w/2, 50)
		else:
			text(str(self.tap_count), 'Arial', 20, self.size.w-50, self.size.h/2)
		if not self.size.w > 320:
			# 'for Bina from Dad'
			text('untuk Bina dari Ayah', 'Arial', 12, self.size.w/2, 20)
		else:
			text('untuk', 'Arial', 12, self.size.w-50, 42)
			text('Bina', 'Arial', 12, self.size.w-50, 30)
			
	def deal(self):
		# animals face
		img_lib1 = ['Rabbit_Face',
		'Mouse_Face',
		'Cat_Face',
		'Dog_Face',
		'Octopus',
		'Bear_Face',
		'Chicken',
		'Cow_Face',
		'Frog_Face',
		'Horse_Face',
		'Tiger_Face',
		'Panda_Face',
		'Pig_Face',
		'Hamster_Face',
		'Koala',
		'Penguin'] # 16 images
		# fruits and plantations
		img_lib2 = ['Aubergine',
		'Banana',
		'Cherries',
		'Corn',
		'Grapes',
		'Red_Apple',
		'Melon',
		'Strawberry',
		'Tangerine',
		'Watermelon',
		'Mushroom',
		'Four_Leaf_Clover',
		'Blossom',
		'Maple_Leaf',
		'Hibiscus',
		'Cactus'] # 16 images
		# various objects
		img_lib3 = ['Star_1',
		'Moon_1',
		'Heart',
		'Car_1',
		'Rocket',
		'Game_Die',
		'Light_Bulb',
		'Basketball',
		'Telephone_Receiver',
		'Soccer_Ball',
		'Tennis_Ball',
		'Closed_Book',
		'Pencil',
		'Key',
		'Lock_2',
		'Bell'] # 16 images
		
		# grid dimension
		img_used = 8 # 8 for 4x4 grid (half number of the grid)
		self.card_used = img_used * 2 # double for card pairs
		
		# randomly select card theme from image library
		img = randint(1,9)
		if img % 3 == 0: # 3,6,9
			images = sample(img_lib1, img_used)
		elif img % 2 == 0: # 2,4,8
			images = sample(img_lib2, img_used)
		else: # 1,5,7
			images = sample(img_lib3, img_used)
		images = images * 2
		shuffle(images)
		for image in images:
			load_image(image)
			
		self.root_layer.sublayers = []
		self.cards = []
		self.selected = []
		
		# adjust card size to device
		card_size = 96 if self.size.w > 700 else 64
		width = (card_size + 4) * 4
		height = (card_size + 4) * (self.card_used / 4)
		
		# adjust to orientation
		if self.size.w > 320:
			offset = Point((self.size.w - height)/2,(self.size.h - width)/2)
		else:
			offset = Point((self.size.w - width)/2,(self.size.h - height)/2)
			
		for i in xrange(len(images)):
			if self.size.w > 320:
				x, y = i/4, i%4
			else:
				x, y = i%4, i/4
				
			card = Layer(Rect(offset.x + x * (card_size + 5), offset.y + y * (card_size + 5), card_size, card_size))
			card.card_image = images[i]
			card.background = Color(0.9, 0.9, 0.9)
			card.stroke = Color(1, 1, 1)
			card.stroke_weight = 4.0
			self.add_layer(card)
			self.cards.append(card)
		self.touch_disabled = False
		self.tap_count = 0
		
	def touch_began(self, touch):
		if self.touch_disabled or len(self.cards) == 0:
			return
		if len(self.selected) == 2:
			self.discard_selection()
			#return
		for card in self.cards:
			if card in self.selected or len(self.selected) > 1:
				continue
			if touch.location in card.frame:
				def reveal_card():
					card.image = card.card_image
					card.animate('scale_x', 1.0, 0.15, completion=self.check_selection)
				self.selected.append(card)
				self.touch_disabled = True
				card.animate('scale_x', 0.0, 0.15, completion=reveal_card)
				card.scale_y = 1.0
				card.animate('scale_y', 0.9, 0.15, autoreverse=True)
				sound.play_effect('Click_1')
				self.tap_count += 1
				break
				
	def discard_selection(self):
		sound.play_effect('Click_2')
		for card in self.selected:
			def conceal(card):
				card.image = None
				card.animate('scale_x', 1.0, 0.15)
			card.animate('scale_x', 0.0, 0.15, completion=partial(conceal, card))
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
		
		# show score rating
		if self.tap_count < self.card_used:
			txt = 'Sakti!' # 'Impossible!'
		elif self.tap_count == self.card_used:
			txt = 'Sempurna!' # 'Perfect!'
		elif self.tap_count <= 1.5*self.card_used:
			txt = 'Hebat!' # 'Excellent!'
		elif self.tap_count <= 2*self.card_used:
			txt = 'Bagus!' # 'Great!'
		elif self.tap_count <= 2.5*self.card_used:
			txt = 'Lumayan!' # 'Good!'
		elif self.tap_count <= 3*self.card_used:
			txt = 'Biasa!' # 'Average!'
		else:
			txt = 'Jelek!' # 'Bad!'
			
		ngomong(txt)
		
		text_layer = TextLayer(txt, 'Futura', font_size)
		text_layer.frame.center(self.bounds.center())
		overlay = Layer(self.bounds)
		overlay.background = Color(0, 0, 0, 0)
		overlay.add_layer(text_layer)
		self.add_layer(overlay)
		overlay.animate('background', Color(0.0, 0.2, 0.3, 0.7))
		text_layer.animate('scale_x', 1.3, 0.3, autoreverse=True)
		text_layer.animate('scale_y', 1.3, 0.3, autoreverse=True)
		self.touch_disabled = True
		self.root_layer.animate('scale_x', 0.0, delay=5.0,
		curve=curve_ease_back_in)
		self.root_layer.animate('scale_y', 0.0, delay=5.0,
		curve=curve_ease_back_in,
		completion=self.new_game)
		
run(Game())

