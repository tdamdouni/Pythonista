# https://gist.github.com/SebastianJarsve/5305895
# -*- coding: utf-8 -*-
# Created by Sebastian Jarsve
# 9. April 2013

from scene import *
from sound import play_effect
from random import randint

def centered_rect(x, y, w, h):
	return Rect(x-w/2, y-h/2, w, h)

class Field(object):
	def __init__(self):
		size = screen_size
		left = 0
		bottom = 0
		right = screen_size.w
		top = screen_size.h
		self.lines = [(left, bottom, left, top), (left, top, right, top), (right, top, right, bottom)]
		
	def draw(self):
		stroke_weight(4)
		stroke(1,1,1)
		for l in self.lines:
			line(*l)


class Player(object):
	def __init__(self):
		self.rect = centered_rect(screen_size.w/2, 50, 100, 20)
		self.lives = 3
		
	def update(self):
		self.rect.x += gravity().x * 50
		self.rect.x = min(screen_size.w - 100, max(0, self.rect.x))
			
	def draw(self):
		fill(1,1,1)
		rect(*self.rect)


class Ball(object):
	def __init__(self):
		self.rect = centered_rect(screen_size.w/2, 60, 20, 20)
		self.vx = randint(-6, 6)
		self.vy = 7
		self.is_moving = False
	
	def collide_with_paddle(self, paddle):
		if self.rect.intersects(paddle.rect):
			self.rect.y = paddle.rect.top()
			self.vy *= -1
			pos = self.rect.center().x - paddle.rect.center().x
			self.vx = pos/10
			play_effect('Jump_3')
			
	def collide_with_block(self, block):
		if self.rect.intersects(block.rect):
			if self.rect.intersects(block.left):
				self.rect.x = block.rect.left()-self.rect.w
				self.vx = -abs(self.vx)
			elif self.rect.intersects(block.right):
				self.rect.x = block.rect.right()
				self.vx = abs(self.vx)
			elif self.rect.intersects(block.top):
				self.rect.y = block.rect.top()
				self.vy = abs(self.vy)
			elif self.rect.intersects(block.bottom):
				self.rect.y = block.rect.bottom()-self.rect.h
				self.vy = -abs(self.vy)
			return True
	
	def update(self, dt):
		self.rect.x += self.vx + dt*10
		self.rect.y += self.vy + dt*10
		if self.rect.right() >= screen_size.w:
			self.rect.x = screen_size.w - self.rect.w
			self.vx *= -1
			play_effect('Jump_5')
		if self.rect.left() <= 0:
			self.rect.x = 0
			self.vx *= -1
			play_effect('Jump_5')
		if self.rect.top() >= screen_size.h:
			self.rect.y = screen_size.h - self.rect.w
			self.vy *= -1 
			play_effect('Jump_5')
	
	def draw(self):
		fill(1,1,0)
		no_stroke()
		ellipse(*self.rect)
		
		
class Block(object):
	def __init__(self, x, y, w, mode=1):
		self.size = Size(w, 30)
		self.rect = Rect(x, y, *self.size)
		self.mode = mode
		if self.mode > 1:
			self.colour = (0.70, 0.70, 0.70)
		else: 
			self.colour = (1,0,0)
		
		top = self.rect.top()
		left = self.rect.left()
		right = self.rect.right()
		bottom = self.rect.bottom()
		
		self.left = Rect(left-5, bottom+5, 5, top-bottom-10)
		self.right = Rect(right, bottom+5, 5, top-bottom-10)
		self.bottom = Rect(left, bottom, right-left, 5)
		self.top = Rect(left, top-5, right-left, 5)
		
	def draw_sides(self):
		fill(0,1,0)
		rect(*self.left)
		rect(*self.right)
		rect(*self.top)
		rect(*self.bottom)
		
	def draw(self):
		stroke_weight(1)
		#no_stroke()
		fill(*self.colour)
		rect(*self.rect)
		#self.draw_sides()
		
		
def random_level(n=7, t=13):
	level = []
	for i in range(n):
		level.append([])
		for j in range(t):
			level[i].append(randint(0, 1))
	return level
		
level = [
         	[[1, 1, 1],
           	 [1, 1, 1],
           	 [1, 1, 1],
           	 [1, 1, 1],
           	 [1, 1, 1]],
			 
			[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
			 [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
			 [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
			 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
			 [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
			 [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
			 [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]],
			 
			[[0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
			 [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
			 [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
			 [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
			 [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
			 [0, 0, 1, 1, 1, 1, 1, 1, 0, 0]],

			[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
			 [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
			 [1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1],
			 [1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1], 
			 [1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1],
			 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
			 
			[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
			 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
			 [1, 				2, 				  1],
			 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
			 
			[[1, 1, 1, 1, 1, 1, 1, 1],
			 [1, 1, 1, 1, 1, 1, 1, 1],
			 [2, 2, 2, 0, 0, 2, 2, 2]],
			 
			 random_level()
		]

class Game(Scene):
	def setup(self):
		self.level = 1
		self.field = Field()
		self.player = Player()
		self.ball = Ball()
		self.blocks = []
		self.spawn_blocks()
		
	def spawn_blocks(self):
		self.solid_blocks = []
		if self.level > len(level):
			lvl = len(level)-1
		else: 
			lvl = self.level-1
		for y in range(len(level[lvl])):
			for x in range(len(level[lvl][y])):
				w = screen_size.w/len(level[lvl][y])
				mode = level[lvl][y][x]
				if level[lvl][y][x] == 1:
					self.blocks.append(Block(x * w, screen_size.h - (y*30+90),
					                         w, mode))
				elif level[lvl][y][x] == 2:
					self.solid_blocks.append(Block(x * w, screen_size.h - (y*30+90),
					                               w, mode))
	
	def draw(self):
		removed_blocks = set()

		text('Lives: {0}'.format(self.player.lives), x=screen_size.w-45, y=screen_size.h-40)
		text('Level: {0}'.format(self.level), x=45, y=screen_size.h-45)
		
		self.field.draw()
		
		self.player.draw()
		self.player.update()
		
		self.ball.draw()
		if self.ball.is_moving:
			self.ball.update(self.dt)
			self.ball.collide_with_paddle(self.player)
		else: 
			self.ball.rect.center(self.player.rect.center().x, self.player.rect.top()+10)
			self.ball.line = (0, 0, 0, 0)
		if self.ball.rect.top() < 0:
			self.player.lives -= 1
			self.ball.is_moving = False
			
		for block in self.blocks:
			block.draw()
			if self.ball.is_moving:
				if self.ball.collide_with_block(block):
					removed_blocks.add(block)
					play_effect('Hit_3')
					
		for solid_block in self.solid_blocks:
			solid_block.draw()
			if self.ball.is_moving:
				if self.ball.collide_with_block(solid_block):
					play_effect('Ding_1')
				
		for removed_block in removed_blocks:
			self.blocks.remove(removed_block)
			
		if len(self.blocks) == 0:
			self.ball.is_moving = False
			self.level += 1
			self.spawn_blocks()
			if self.level >= len(level):
				level[-1] = random_level()
				self.spawn_blocks()
		
		if self.player.lives == 0:
			main_scene.switch_scene(GameOver())
	
	def touch_began(self, touch):
		if not self.ball.is_moving:
			self.ball.is_moving = True
			
			
class GameOver(Scene):
	def setup(self):
		self.field = Field()
		self.button = Button(Rect(screen_size.w/2-100, screen_size.h/2-50, 200, 100), 'Restart')
		self.button.action = self.restart
		self.add_layer(self.button)
	
	def restart(self):
		main_scene.switch_scene(Game())
		
	def draw(self):
		self.field.draw()
		self.button.draw()
		no_tint()
		text('Game Over', x=screen_size.w/2, y=screen_size.h/4*3, font_size=64)
		
		
class MultiScene(Scene):
	def __init__(self, start_scene):
		self.active_scene = start_scene
		run(self, PORTRAIT)
	def switch_scene(self, new_scene):
		self.active_scene = new_scene
		self.setup()
	def setup(self):
		global screen_size
		screen_size = self.size
		self.active_scene.add_layer = self.add_layer
		self.active_scene.size = self.size
		self.active_scene.bounds = self.bounds
		self.active_scene.setup()
	def draw(self):
		background(0.00, 0.25, 0.50)
		self.active_scene.touches = self.touches
		self.active_scene.dt = self.dt
		self.active_scene.draw()
	def touch_began(self, touch):
		self.active_scene.touch_began(touch)
	def touch_moved(self, touch):
		self.active_scene.touch_moved(touch)
	def touch_ended(self, touch):
		self.active_scene.touch_ended(touch)
		
main_scene = MultiScene(Game())