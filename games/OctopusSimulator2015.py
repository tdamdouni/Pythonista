# coding: utf-8

# https://gist.github.com/J-Behemoth/bcb8d727fcb7d7fc5224

#Octopus Simulator 2015
#by Jackson Laumann
#
#Thank you for getting this and looking at the code,
#thanks again and have fun!

from scene import *
from random import *
from sound import *
import pickle
octosize = 100
title = 0
chomp = 0
points = 0
attack = 0
moby = randint(100,650)
swim = randint(100, 350)
highscore = 0
new = 0
bubbles = 0

class game (Scene):
	def setup(self):
		octosize = 100
		title = 0
		chomp = 0
		points = 0
		attack = 0
		global on, speed
		on = 0
		speed = 0.2
		moby = randint(100,650)
		global blubblex
		blubblex = randint(10,1020)
		highscore = 0
		global inkon, inkfade
		inkon = 99
		inkfade = 1
		self.x = self.size.w * 0.5
		self.y = self.size.h * 0.5
		self.ocean = Layer(Rect(0, 0, 1100, 1000))
		self.ocean.background = Color(0.00, 1.00, 1.00)
		self.ocean.alpha = (0.7)
		self.blubble = Layer(Rect(blubblex, 50, 25, 25))
		self.blubble.alpha = (0.7)
		self.blubble.image = 'White_Circle'
		global fishx,fishy
		fishx = randint(0,900)
		fishy = randint(120,650)
		self.food = Layer(Rect(fishx, fishy, 50, 50))
		self.food.image = 'Tropical_Fish'
		self.octopus = Layer(Rect(self.x, self.y, 100, 100))
		self.octopus.tint = (1.00, 1.00, 0.00)
		self.octopus.image = 'Octopus'
		self.mob = Layer(Rect(1024, moby, 200, 200))
		self.mob.image = 'Fish'
		self.shell = Layer(Rect(100, 50, 100, 100))
		self.shell.image = 'Spiral_Shell'
		self.shell.alpha = (1)
		octopusRect = Rect(self.x, self.y, 100, 100)
		foodRect = Rect(fishx, fishy, 50, 50)
		mobRect = Rect(self.mob.frame.x + 20, self.mob.frame.y + 30, 140, 150)
	def draw(self):
		background(0.00, 0.25, 0.50)
		self.ocean.draw()
		self.blubble.update(self.dt)
		self.blubble.draw()
		g = gravity()
		self.x += g.x * 13
		self.y += g.y * 13
		self.x = min(self.size.w - 100, max(0, self.x))
		self.y = min(self.size.h - 100, max(90, self.y))
		fill(1.00, 0.95, 0.60)
		rect(0, 0, 1100, 100)
		stroke(0, 0, 0)
		stroke_weight(1)
		line(0,100, 1100,100)
		global title
		if title == 0:
			global on, points, new
			if on == 0:
				self.shell.draw()
				rotate(45)
				image('Anchor', 400, -350, 150, 150)
				rotate(-45)
				image('Sailboat', 850, 80, 300, 300)
				tint(0.00, 0.50, 0.50)
				text('Octopus Simulator 2015', 'ChalkboardSE-Bold', 80, 512, 650, 5)
				tint(1.00, 1.00, 0.40)
				text('by Jackson Laumann', 'ChalkboardSE-Bold', 40, 512, 575, 5)
				tint(0.50, 1.00, 0.00)
				text('Swim on small fish to eat', 'ChalkboardSE-Bold', 40, 513, 500, 5)
				text('them and get points', 'ChalkboardSE-Bold', 40, 512, 450, 5)
				tint(1.00, 0.00, 0.00)
				text('avoid the big fish', 'ChalkboardSE-Bold', 40, 512, 400, 5)
				tint(0, 0, 0)
				text('tap to ink, has a cooldown', 'ChalkboardSE-Bold', 40, 512, 350, 5)
				tint(1.00, 0.40, 0.40)
				text('tilt the device to move', 'ChalkboardSE-Bold', 40, 512, 300, 5)
				tint(0.50, 1.00, 0.00)
				text('tap to begin', 'ChalkboardSE-Bold', 45, 512, 250, 5)
				tint(1, 1, 1)
			else:
				self.shell.draw()
				rotate(45)
				image('Anchor', 400, -350, 150, 150)
				rotate(-45)
				image('Sailboat', 850, 80, 300, 300)
				tint(1, 0, 0)
				text('GAME OVER', 'ChalkboardSE-Bold', 64, 512, 500, 5)
				tint(0.50, 1.00, 0.00)
				text('You got %d points' % points, 'ChalkboardSE-Bold', 40, 512, 400, 5)
				tint(1,1,1)
				global highscore, new
				try:
					with open('octoHigh', 'r') as f:
						highscore = pickle.load(f)
				except IOError:
					highscore = 0
				if points > highscore:
					highscore = points
					new = 1
					play_effect('Powerup_1')
				if new == 1:
					tint(0.00, 0.50, 0.25)
					text('New Highscore!', 'ChalkboardSE-Bold', 45, 512, 350, 5)
				tint(1.00, 1.00, 0.40)
				text('Highscore: %d' % highscore, 'ChalkboardSE-Bold', 40, 512, 300, 5)
				tint(1, 1, 1)
				with open('octoHigh', 'w+') as f:
					pickle.dump(highscore, f)
				text('tap to retry', 'ChalkboardSE-Bold', 40, 512, 250, 5)
		else:
			on = 1
			octopusRect = Rect(self.x, self.y, 100, 50)
			global fishx,fishy
			foodRect = Rect(fishx, fishy, 50, 50)
			self.food.update(self.dt)
			self.food.draw()
			foodRect
			global octosize
			self.octopus = Layer(Rect(self.x, self.y, octosize, octosize))
			self.octopus.image = 'Octopus'
			self.octopus.update(self.dt)
			self.octopus.draw()
			octopusRect
			self.shell.draw()
			rotate(45)
			image('Anchor', 400, -350, 150, 150)
			rotate(-45)
			image('Sailboat', 850, 80, 300, 300)
			global inkon, speed
			score = '%d' % points
			text(score, 'ChalkboardSE-Bold', 40, 512, 730, 5)
			self.mob.update(self.dt)
			self.mob.draw()
			mobRect = Rect(self.mob.frame.x, self.mob.frame.y + 25, 150, 150)
			mobRect
			if inkon < 40:
				global inkfade
				inkfade = inkfade - 0.018
				fill(0, 0, 0, inkfade)
				ellipse(self.x - 50, self.y - 50, 200, 200)
			if mobRect.intersects(foodRect):
				play_effect('Hit_2')
				tint(0.50, 1.00, 0.00)
				text('Chomp!', 'Chalkduster', 32, mobRect.x, mobRect.y, 5)
				fishx = randint(0,900)
				fishy = randint(120,650)
				self.food = Layer(Rect(fishx, fishy, 50, 50))
				self.food.image = 'Tropical_Fish'
			if octopusRect.intersects(mobRect):
				if inkon > 40:
					title = 0
					play_effect('Explosion_4')
			if octopusRect.intersects(foodRect):
				tint(0.50, 1.00, 0.00)
				text('Chomp!', 'Chalkduster', 32, octopusRect.x, octopusRect.y, 5)
				global chomp
				global attack
				global swim
				chomp = chomp + 1
				if chomp > 10:
					play_effect('Coin_2')
					fishx = randint(0,900)
					fishy = randint(120,650)
					self.food = Layer(Rect(fishx, fishy, 50, 50))
					self.food.image = 'Tropical_Fish'
					points = points + 1
					chomp = 0
			global bubbles
			attack = attack + 1
			bubbles = bubbles + 1
			if speed > 0.13:
				speed = speed - 0.00001
			if inkon < 100:
				inkon = inkon + 0.15
			tint(0, 0, 0)
			text('Ink', 'ChalkboardSE-Bold', 40, 835, 55, 5)
			stroke(0, 0, 0)
			stroke_weight(5)
			fill(0.80, 0.80, 0.80)
			rect(870, 25, 110, 50)
			stroke_weight(0)
			fill(0, 0, 0, 100)
			if inkon > 100:
				fill(0.80, 1.00, 0.40)
			elif inkon > 80:
				fill(1.00, 1.00, 0.00)
			elif inkon > 65:
				fill(1.00, 0.80, 0.00)
			elif inkon > 50:
				fill(1.00, 0.50, 0.00)
			elif inkon > 25:
				fill(1.00, 0.30, 0.00)
			else:
				fill(1.00, 0.00, 0.00)
			rect(875, 30, inkon, 40)
			if attack == swim:
				self.mob.update(self.dt)
				play_effect('Woosh_2')
			if attack > swim - 1:
				self.mob.draw()
				global moby
				new_frame = Rect(-250, moby ,200,200)
				self.mob.animate('frame', new_frame, duration=speed)
			if attack > 500:
				new_frame = Rect(1024, moby ,200,200)
				self.mob.animate('frame', new_frame, duration=0)
				moby = randint(100,650)
				swim = randint(100, 350)
				attack = 0
			if bubbles == 1:
				self.blubble.update(self.dt)
			if bubbles > 0:
				fill(1, 1, 1, 0.7)
				self.blubble.alpha = (0.7)
				self.blubble.draw()
				global blubblex
				new_frame = Rect(blubblex, 800,25,25)
				self.blubble.animate('frame', new_frame, duration=0.12)
			if bubbles > 60:
				blubblex = randint(10,1020)
				new_frame = Rect(blubblex, 50,25,25)
				self.blubble.animate('frame', new_frame, duration=0)
				bubbles = 0
	def touch_began(self, touch):
		global title, on, points, chomp, attack, moby, new, inkon, inkfade, speed, swim
		if title == 0 and on == 0:
			title = 1
			points = 0
			play_effect('Woosh_1')
		elif title == 0:
			new = 0
			inkon = 0
			inkfade = 1
			octosize = 100
			chomp = 0
			points = 0
			attack = 0
			speed = 0.2
			swim = randint(100, 350)
			moby = randint(100,650)
			highscore = 0
			self.x = self.size.w * 0.5
			self.y = self.size.h * 0.5
			self.ocean = Layer(Rect(0, 0, 1100, 1000))
			self.ocean.background = Color(0.00, 1.00, 1.00)
			self.ocean.alpha = (0.7)
			global fishx,fishy
			fishx = randint(0,900)
			fishy = randint(120,650)
			self.food = Layer(Rect(fishx, fishy, 50, 50))
			self.food.image = 'Tropical_Fish'
			self.octopus = Layer(Rect(self.x, self.y, 100, 100))
			self.octopus.image = 'Octopus'
			self.mob = Layer(Rect(1024, moby, 200, 200))
			self.mob.image = 'Fish'
			octopusRect = Rect(self.x, self.y, 100, 100)
			foodRect = Rect(fishx, fishy, 50, 50)
			mobRect = Rect(self.mob.frame.x, self.mob.frame.y + 25, 150, 150)
			on = 0
			title = 0
		elif on == 1 and inkon > 100:
			inkon = 0
			play_effect('Spaceship')
			inkfade = 1
			
run(game(),LANDSCAPE)

