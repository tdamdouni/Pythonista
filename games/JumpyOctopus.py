from scene import *
from PIL import Image
import sound
import random

GAME_READY = 0
GAME_PLAY = 1
GAME_DYING = 2
GAME_DEAD = 3

FLOOR_IMGS = ['Ear_Of_Rice', 'Herb', 'Snail', 'Spiral_Shell', 'Turtle', 'Anchor', 'Pile_Of_Poo', 'Sailboat', 'Speedboat']
BACK_IMGS = ['Blowfish', 'Dolphin', 'Fish', 'Tropical_Fish', 'Whale']


class GameEnvironment(object):
	def __init__(self, x, y, w, h):
		self.playfield = Rect(x, y, w, h)
		self.gravity =				int(h *-3.000)			# 3000
		self.scroll = 				int(h * 0.300)			# 300
		self.float_max = 			int(h * 0.300)			# 300
		self.float_min =      int(h * 0.050)			# 50
		self.jump = 					int(h * 0.800)			# 800
		self.gap = 						int(h * 0.360)			# 360
		self.ground_height =  int(h * 0.100)			# 100
		self.tower_width =    int(h * 0.140)			# 140
		self.tower_cap = 			int(h * 0.065)			# 65
		self.tower_gap = (self.playfield.w - (self.tower_width * 2)) / 2
		self.tower_min_height = self.tower_cap
		self.tower_max_height = self.playfield.h - self.ground_height - self. tower_cap - self.tower_gap
		self.player_width = 	int(h * 0.080)			# 80
		self.player_height = 	int(h * 0.080)			# 80
		self.player_x = 			int(h * 0.200)			# 200
		self.player_y = self.playfield.h / 2 + self.ground_height
		self.bubble_min = 		int(h * 0.002)			# 2
		self.bubble_max = 		int(h * 0.020)			# 20
		self.floor_min =  		int(h * 0.040)			# 40
		self.floor_max =  		int(h * 0.128)			# 128
		self.back_min =  			int(h * 0.020)			# 20
		self.back_max =  			int(h * 0.040)			# 40
		self.text_x = w / 2
		self.text_1_y = 0.9 * h
		self.text_2_y = 0.6 * h
		self.text_3_y = 0.4 * h
		self.font_size =  		int(h * 0.064)			#  64
		self.font = 'AvenirNext-Heavy'
		self.score = 0
		self.best = 0
		self.crash = False
		self.gametime = 0
		self.deadtime = 0
		self.state = GAME_READY
		
class Bubble(object):
	def __init__(self, x, y, w, h, float):
		self.bounds = Rect(x, y, w, h)
		self.float = float
		self.alpha = random.random()
		self.img = 'White_Circle'
		
	def draw(self):
		tint(1, 1, 1, self.alpha)
		image(self.img, self.bounds.x, self.bounds.y, self.bounds.w, self.bounds.h)
		
class Player(object):
	def __init__(self, x, y, w, h):
		self.bounds = Rect(x, y, w, h)
		img = Image.open('Octopus').transpose(Image.FLIP_LEFT_RIGHT)
		self.img = load_pil_image(img)
		self.velocity = 0
		self.jumped = False
		
	def draw(self):
		tint(1.00, 1.00, 1.00)
		image(self.img, self.bounds.x, self.bounds.y, self.bounds.w, self.bounds.h)
		
class FloorSprite(object):	
	def __init__(self, env):
		self.env = env
		self.set_random_bounds()
		self.set_random_image()
		
	def set_random_image(self):
		img = Image.open(FLOOR_IMGS[random.randint(0, len(FLOOR_IMGS) - 1)])
		if(random.random > 0.5):
			img = img.transpose(Image.FLIP_LEFT_RIGHT)
		self.img = load_pil_image(img)

	def set_random_bounds(self):
		env = self.env
		size = random.randint(env.floor_min, env.floor_max)
		y = random.randint(env.playfield.bottom(), env.ground_height)
		x = random.randint(env.playfield.left(), env.playfield.right() + env.playfield.w)
		self.bounds = Rect(x, y, size, size)
		
	def draw(self):
		tint(1,1,1)
		image(self.img, self.bounds.x, self.bounds.y, self.bounds.w, self.bounds.h)
		
class BackgroundSprite(object):
	def __init__(self, env):
		self.env = env
		self.velocity = env.scroll / 4
		self.set_random_bounds()
		self.set_random_image()

	def set_random_image(self):
		img = Image.open(BACK_IMGS[random.randint(0, len(BACK_IMGS) - 1)])
		self.velocity = random.randint(self.env.scroll / 4, self.env.scroll / 2)
		if(random.random() > 0.5):
			img = img.transpose(Image.FLIP_LEFT_RIGHT)
			self.velocity *= -1
		self.img = load_pil_image(img)

	def set_random_bounds(self):
		env = self.env
		size = random.randint(env.back_min, env.back_max)
		y = random.randint(env.ground_height, env.playfield.top() - size)
		if self.velocity < 0:
			x = env.playfield.left()
		else:
			x = env.playfield.right()
		self.bounds = Rect(x, y, size, size)
		
	def draw(self):
		tint(1,1,1)
		image(self.img, self.bounds.x, self.bounds.y, self.bounds.w, self.bounds.h)
				
class Ground(object):
	def __init__(self, x, y, w, h):
		self.bounds = Rect(x, y, w, h)
	
	def draw(self):
		stroke_weight(4)
		stroke(0.00, 0.00, 0.00)
		fill(0.50, 0.25, 0.00)
		rect(self.bounds.x, self.bounds.y, self.bounds.w, self.bounds.h)
		
class Tower(object):
	def __init__(self, x, env):
		self.x = x
		self.env = env
		self.create_towers_and_caps()
		
	def set_x(self, x):
		self.x = x
		self.lower_tower.x = x + 6
		self.lower_cap.x = x
		self.upper_tower.x = x + 6
		self.upper_cap.x = x
		
	def right(self):
		return self.lower_tower.right()
	
	def left(self):
		return self.lower_tower.left()
		
	def create_towers_and_caps(self):
		self.passed = False
		height = random.randint(self.env.tower_min_height, self.env.tower_max_height)
		self.lower_tower = Rect(self.x + 6, self.env.ground_height, self.env.tower_width - 12, height)
		self.lower_cap = Rect(self.x, self.env.ground_height + height - self.env.tower_cap, self.env.tower_width, self.env.tower_cap)
		self.upper_tower =  Rect(self.x + 6, height + self.env.gap, self.env.tower_width - 12, self.env.playfield.h - height + self.env.gap)
		self.upper_cap = Rect(self.x, height + self.env.gap, self.env.tower_width, self.env.tower_cap)
		
	def intersects(self, r):
		return self.lower_tower.intersects(r) or self.upper_tower.intersects(r)
		
	def draw(self):
		stroke_weight(4)
		stroke(0.00, 0.50, 0.25)
		stroke(0.20, 0.20, 0.00)
		fill(0.00, 1.00, 0.00)
		fill(0.50, 0.50, 0.00)
		rect(self.lower_tower.x, self.lower_tower.y, self.lower_tower.w, self.lower_tower.h)
		rect(self.lower_cap.x, self.lower_cap.y, self.lower_cap.w, self.lower_cap.h)
		rect(self.upper_tower.x, self.upper_tower.y, self.upper_tower.w, self.upper_tower.h)
		rect(self.upper_cap.x, self.upper_cap.y, self.upper_cap.w, self.upper_cap.h)

class Game(object):
	def __init__(self, x, y, w, h):
		self.env = GameEnvironment(x, y, w, h)
		self.game_setup()
		
	def game_setup(self):
		self.env.score = 0
		self.env.crash = False
		self.env.state = GAME_READY
		self.create_game_objects()
		
	def create_game_objects(self):
		self.player = Player(self.env.player_x, self.env.player_y, self.env.player_width, self.env.player_height)
		self.ground = Ground(self.env.playfield.x, self.env.playfield.y, self.env.playfield.w, self.env.ground_height)
		self.towers = []
		x = self.env.playfield.w * 2
		for t in range(3):
			self.towers.append(Tower(x, self.env))
			x += self.env.tower_width + self.env.tower_gap
		self.bubbles = []
		for t in range(10):
			d = random.randint(0, 20)
			self.bubbles.append(Bubble(random.randint(0, self.env.playfield.w), random.randint(0, self.env.playfield.h), d, d,random.randint(self.env.float_min, self.env.float_max)))
		self.floor_sprites = []
		for t in range(1):
			self.floor_sprites.append(FloorSprite(self.env))
		self.background_sprites = []
		for t in range(2):
			self.background_sprites.append(BackgroundSprite(self.env))
			
	def move_player(self, dt):
		if(self.env.state == GAME_DEAD):
			return
		elif((self.env.state == GAME_READY) and (self.player.bounds.y < (self.env.playfield.h / 2)) or self.player.jumped):
			self.player.jumped = False
			self.player.velocity = self.env.jump
		else:
			self.player.velocity = self.player.velocity + self.env.gravity * dt
		self.player.bounds.y += self.player.velocity * dt
		
	def move_towers(self, dt):
		if(self.env.state == GAME_PLAY):
			move = self.env.scroll * dt
			for tower in self.towers:
				tower.set_x(tower.x - move)
				if tower.right() < self.env.playfield.x:
					tower.set_x(self.env.playfield.w + self.env.tower_gap)
					tower.create_towers_and_caps()
				
	def move_bubbles(self, dt):
		if(self.env.state == GAME_DEAD):
			return
		for bubble in self.bubbles:
			if (bubble.bounds.bottom() > self.env.playfield.top()) or (bubble.bounds.left() < self.env.playfield.left()):
				x = random.randint(self.env.playfield.left(), self.env.playfield.right() + self.env.playfield.w)
				y = self.env.playfield.bottom() - random.randint(0, self.env.bubble_max)
				d = random.randint(self.env.bubble_min, self.env.bubble_max)
				bubble.bounds = Rect(x, y, d, d)
				bubble.float = random.randint(self.env.float_min, self.env.float_max)
			bubble.bounds.y += bubble.float * dt
			if(self.env.state <> GAME_DYING):
				bubble.bounds.x -= self.env.scroll * dt
				
	def move_floor_sprites(self, dt):
		if(self.env.state == GAME_READY) or (self.env.state == GAME_PLAY):
			move = self.env.scroll * dt
			for sprite in self.floor_sprites:
				sprite.bounds.x -= move
				if sprite.bounds.right() < self.env.playfield.left():
					sprite.set_random_image()
					sprite.set_random_bounds()
					sprite.bounds.x = random.randint(self.env.playfield.right(), self.env.playfield.right() + self.env.playfield.w)
					
	def move_background_sprites(self, dt):
		if(self.env.state == GAME_READY) or (self.env.state == GAME_PLAY):
			for sprite in self.background_sprites:
				move = sprite.velocity * dt
				sprite.bounds.x -= move
				if(sprite.bounds.right() < self.env.playfield.left()) or (sprite.bounds.left() > self.env.playfield.right()):
					sprite.set_random_image()
					sprite.set_random_bounds()

	def update_score(self):
		if(self.env.state == GAME_PLAY):
			for tower in self.towers:
				if tower.passed == False:
					if tower.left() < self.player.bounds.right():
						tower.passed = True
						self.env.score += 1
						sound.play_effect('Coin_1')
						
	def player_dead(self):
		self.env.state = GAME_DEAD
		self.env.dead_time = self.env.game_time
		if self.env.score > self.env.best:
			self.env.best = self.env.score
	
	def collision_detect(self):
		if(self.env.state == GAME_PLAY):
			if self.player.bounds.bottom() < self.ground.bounds.top():
				sound.play_effect('Crashing')
				self.env.crash = True
				self.player_dead()
		elif(self.env.state == GAME_DYING):
			if self.player.bounds.bottom() < self.ground.bounds.top():
				self.player_dead()			
		if self.env.state == GAME_PLAY:
			if self.player.bounds.bottom() > self.env.playfield.top():
					self.env.crash = True
					self.env.state = GAME_DYING
			else:
				for tower in self.towers:
					if tower.intersects(self.player.bounds):
						sound.play_effect('Crashing')
						self.env.crash = True
						self.env.state = GAME_DYING
					
	def text_shadow(self, s, y):
		tint(0, 0, 0)
		text(s, self.env.font, self.env.font_size, self.env.text_x + 4, y - 4)
		tint(1, 1, 1)
		text(s, self.env.font, self.env.font_size, self.env.text_x, y)
					
	def draw(self):
		if(self.env.crash):
			background(1, 1, 1)
			self.env.crash = False
		else:
			background(0.00, 0.50, 0.50)
			for bubble in self.bubbles:
				bubble.draw()	
			for sprite in self.background_sprites:
				sprite.draw()
			self.ground.draw()
			for tower in self.towers:
				tower.draw()
			self.player.draw()
			for sprite in self.floor_sprites:
				sprite.draw()
			tint(0, 0, 0)
			if(self.env.state == GAME_READY):
				self.text_shadow("Tap to Start!", self.env.text_2_y)
			elif((self.env.state == GAME_PLAY) or (self.env.state == GAME_DYING) or (self.env.state == GAME_READY)):
				self.text_shadow(str(int(self.env.score)), self.env.text_1_y)
			elif(self.env.state == GAME_DEAD):
				self.text_shadow("Score : " + str(int(self.env.score)), self.env.text_2_y)
				self.text_shadow("Best  : " + str(int(self.env.best)), self.env.text_3_y)
				
	def loop(self, dt, t):
		self.env.game_time = t
		self.move_player(dt)
		self.move_towers(dt)
		self.move_bubbles(dt)
		self.move_floor_sprites(dt)
		self.move_background_sprites(dt)
		self.update_score()
		self.collision_detect()
		self.draw()
		
	def screen_tapped(self):
		if(self.env.state == GAME_READY):
			self.env.state = GAME_PLAY
		if(self.env.state == GAME_PLAY):
			self.player.jumped = True
			sound.play_effect('Boing_1')
		elif(self.env.state == GAME_DEAD):
			if(self.env.dead_time + 0.5 < self.env.game_time):
				self.game_setup()			

class MyScene (Scene):
	def setup(self):
		self.game = Game(self.bounds.x, self.bounds.y, self.bounds.w, self.bounds.h)
	
	def draw(self):
		self.game.loop(self.dt, self.t)
	
	def touch_began(self, touch):
		self.game.screen_tapped()
	
run(MyScene(), PORTRAIT)
