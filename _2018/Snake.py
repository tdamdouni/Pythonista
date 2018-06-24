# Snake
#
# Controls: Turn left or right by tapping the
# left or right half of the screen.

from scene import *
from sound import load_effect, play_effect
from random import randint
import pickle
from functools import partial

class Game (Scene):
	def setup(self):
		w, h = self.size.as_tuple()
		self.field = Rect(16, (h - w - 44) / 2 + 16, w - 32, w - 32)
		for effect in ['Coin_1', 'Explosion_3', 'Powerup_2']:
			load_effect(effect)
		self.load_highscore()
		self.new_game()
	
	def draw(self):
		self.draw_background()
		segments = self.get_snake_segments()
		self.draw_snake(segments)
		if self.paused:
			return
		self.move_snake(segments)
	
	def touch_began(self, touch):
		directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
		if touch.location.x > self.size.w / 2:
			direction_index = (directions.index(self.direction) + 1) % 4
		else:
			direction_index = directions.index(self.direction) - 1
		self.next_direction = directions[direction_index]
	
	def new_game(self):
		self.items = set()
		self.joints = []
		self.joints.append(Point(self.size.w / 2, 256)) #head
		self.joints.append(Point(self.size.w / 2, 160)) #tail
		self.direction = (0, 1) #up
		self.next_direction = None
		self.grow = 0
		self.speed = 3
		self.paused = False
		self.score = 0
		for i in xrange(3): self.add_item()
	
	def game_over(self):
		play_effect('Explosion_3')
		self.paused = True
		if self.score > self.highscore:
			self.highscore = self.score
			self.save_highscore()
		self.delay(2.0, self.new_game)
	
	def draw_background(self):
		#Draw field and scores:
		background(0, 0, 0)
		tint(1, 1, 1)
		text(str(self.score), 'Futura', 40, self.size.w/2, self.size.h - 50)
		if self.score < self.highscore:
			tint(0.6, 0.6, 0.6)
		else:
			tint(0, 1, 0)
		text('Highscore: ' + str(self.highscore), 
		     'Futura', 24, self.size.w/2, 50)
		fill(0, 0.45, 0.65)
		rect(*self.field.as_tuple())
		#Draw collectable items:
		fill(1, 0, 0)
		for item in self.items:
			ellipse(item.x - 10, item.y - 10, 20, 20)
	
	def get_snake_segments(self):
		#Calculate the rectangles that connect the joints:
		segments = []
		prev_joint = None
		for joint in self.joints:
			if prev_joint is not None:
				p1 = prev_joint
				p2 = joint
				if p1.x == p2.x:
					segments.append(Rect(p1.x - 15, p1.y, 30, p2.y - p1.y))
				else:
					segments.append(Rect(p1.x, p1.y - 15, p2.x - p1.x, 30))
			prev_joint = joint
		return segments
	
	def draw_snake(self, segments):
		fill(1, 0.8, 0.25)
		stroke(0, 0, 0)
		stroke_weight(1)
		for joint in self.joints:
			ellipse(joint.x - 15, joint.y - 15, 30, 30)
		for segment in segments:
			rect(*segment.as_tuple())
		stroke_weight(0)
		for joint in self.joints:
			ellipse(joint.x - 14, joint.y - 14, 28, 28)
		#Draw eyes:
		fill(0, 0, 0)
		stroke(1, 1, 1)
		stroke_weight(2)
		head = self.joints[0]
		if abs(self.direction[0]) > 0:
			ellipse(head.x - 10 * self.direction[0] - 4, head.y + 2, 8, 8)
			ellipse(head.x - 10 * self.direction[0] - 4, head.y - 10, 8, 8)
		else:
			ellipse(head.x + 2, head.y - 10 * self.direction[1] - 4, 8, 8)
			ellipse(head.x - 10, head.y - 10 * self.direction[1] - 4, 8, 8)
		stroke_weight(0)
	
	def move_snake(self, segments):
		hx = self.joints[0].x
		hy = self.joints[0].y
		tx = self.joints[-1].x
		ty = self.joints[-1].y
		collected = set()
		for i in xrange(self.speed):
			#Move head:
			hx += self.direction[0]
			hy += self.direction[1]
			if self.next_direction is not None:
				if hx % 32 == 0 and hy % 32 == 0:
					self.joints.insert(1, Point(hx, hy))
					self.direction = self.next_direction
					self.next_direction = None
			#Don't move the tail while growing:
			if self.grow > 0:
				self.grow -= 1
			else:
				#Move the tail towards the last joint:
				tx += cmp(self.joints[-2].x, tx)
				ty += cmp(self.joints[-2].y, ty)
				#When the joint is reached, remove it:
				if tx == self.joints[-2].x and ty == self.joints[-2].y:
					del self.joints[-1]
			#Update head and tail positions:
			self.joints[0].x = hx
			self.joints[0].y = hy
			self.joints[-1].x = tx
			self.joints[-1].y = ty
			#Check collisions:
			head_rect = Rect(hx - 15, hy - 15, 30, 30)
			for segment in segments[2:]:
				if head_rect.intersects(segment):
					self.game_over()
			if hx < self.field.left() + 16 or hx > self.field.right() - 16:
				self.game_over()
			elif hy < self.field.bottom() + 16 or hy > self.field.top() - 16:
				self.game_over()
			#Collect items:
			for item in self.items:
				if hx == item.x and hy == item.y:
					collected.add(item)
		self.collect_items(collected)
	
	def collect_items(self, collected):
		if len(collected) > 0: play_effect('Coin_1')
		for item in collected:
			self.items -= collected
			self.grow += 32
			self.score += 10
			self.add_item()
		#Speed up for every 10 collected items:
		if len(collected) > 0 and self.score % 100 == 0:
			self.speed = min(8, self.speed + 1)
			play_effect('Powerup_2')
			#Pause the game for 1 second when the speed is increased:
			self.paused = True
			self.delay(1.0, partial(setattr, self, 'paused', False))
	
	def add_item(self):
		x = randint(0, int(self.field.w / 32) - 1) * 32 + 32
		y = randint(0, int(self.field.h / 32) - 1) * 32 + self.field.y + 16
		self.items.add(Point(x, y))
	
	def load_highscore(self):
		try:
			with open('snake_highscore', 'r') as f:
				self.highscore = pickle.load(f)
		except IOError:
			self.highscore = 0
	
	def save_highscore(self):
		with open('snake_highscore', 'w+') as f:
			pickle.dump(self.highscore, f)

run(Game(), PORTRAIT)
