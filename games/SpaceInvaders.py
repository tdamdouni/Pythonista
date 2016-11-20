# https://gist.github.com/davebang/6113246

# Space Invaders clone
# by davebang

from scene import *
from time import sleep
from console import *
import sound
from random import randint

screen_size = Size()
screen_factor = 0.0

class Intro (Scene):
	# draw scene and text
	def draw(self):
		background(0.2,0,0.2)
		
		tint(0.75,0.2,0.4)
		text('SPACE INVADERS', x=(screen_size.w/2), y=(screen_size.h/20) * 18, font_size=48*screen_factor)
		
		tint(0.75,0.2,0.4)
		text('       Drag one finger to move.\n     Tap second finger to shoot.\nHigher enemies give more points.', x=(screen_size.w/2), y=(screen_size.h/20) * 10, font_size=32*screen_factor)
		
		tint(0.75,0.2,0.4)
		text('TAP TO BEGIN', x=(screen_size.w/2), y=(screen_size.h/12) * 2, font_size=32*screen_factor)
	
	# update is called but does nothing
	def update(self, dt):
		pass
	
	# on touch, begin game
	def touch_began(self, touch):
		main_scene.switch_scene(Game)
		

class Game (Scene):
	def setup(self):
		# pre-load sounds
		sound.load_effect('Laser_1')
		sound.load_effect('Explosion_2')
		sound.load_effect('Explosion_4')
		sound.load_effect('Laser_6')
		
		# main layer
		self.layer = Layer(Rect(0, 0, screen_size.w, screen_size.h))
		
		# score
		self.score = 0
		
		# ship sprite
		self.ship = Layer(Rect((screen_size.w / 2) - 50, 
		                       (screen_size.h / 20) * 2,
		                       (100 * screen_factor),
		                       (100 * screen_factor)))
		
		self.ship.image = 'Red_Triangle_1'
		
		self.ship.alpha = 1.0
		self.ship.blendmode = BLEND_ADD
		
		self.layer.add_layer(self.ship)
		
		# ship's laser sprite
		self.laser = Layer(Rect((screen_size.w / 2) - 3, 
		                       (screen_size.h / 20) * 4,
		                        6 * screen_factor, 20 * screen_factor))
		
		self.laser.background = Color(1,1,1,1)
		self.laser.alpha = 0
		
		self.layer.add_layer(self.laser)
		
		# firing - is player currently firing?
		self.firing = False
		
		# space monster
		self.space_monster = []
		self.space_monster_move_x = []
		self.space_monster_laser = []
		self.space_monster_firing =[]
		
		self.space_monster_fire_rate = 400
		self.space_monster_max_speed = 2
		
		for i in range(5):
			# space monster sprite
			space_monster = Layer(Rect(0, 
		                       			(screen_size.h / 9) * (2+(5-i)),
		                     				(100 * screen_factor),
		                      		  (100 * screen_factor)))
		
			space_monster.image = 'Alien_Monster'
		
			space_monster.alpha = 0
			space_monster.blendmode = BLEND_ADD
			
			self.space_monster.append(space_monster)
			
			self.layer.add_layer(self.space_monster[i])
			
			# move x is current movement on x axis
			self.space_monster_move_x.append(randint(-3, 3))
			
			# don't stop moving
			if(self.space_monster_move_x[i] == 0):
				self.space_monster_move_x[i] = 1
				
			# space monster laser
			space_monster_laser = Layer(Rect(0, 0, 6 * screen_factor, 20 * screen_factor))
		
			space_monster_laser.background = Color(1,1,1,1)
			space_monster_laser.alpha = 0
			
			self.space_monster_laser.append(space_monster_laser)
		
			self.layer.add_layer(self.space_monster_laser[i])
			
			self.space_monster_firing.append(False)
			
	def update(self, dt):
		self.layer.update(dt)
		
		# on one finger touch - move ship	
		if(len(self.touches) == 1):
				touch = self.touches[self.touches.keys()[0]]
				
				# move ship towards touch location
			  # only move ship if relative touch location is greater than 5 pixels/points from ship
				if(abs(self.ship.frame.x - (touch.location.x - (45 * screen_factor))) > (5 * screen_factor)):
					if(self.ship.frame.x < touch.location.x - (45 * screen_factor)):
						# the further the touch location, the faster the ship should move
						self.ship.frame.x += (3 + (abs(self.ship.frame.x - (touch.location.x - (45 * screen_factor))) / (screen_size.w / 64))) * screen_factor
					else:
						# the further the touch location, the faster the ship should move
						self.ship.frame.x -= (3 + (abs(self.ship.frame.x - (touch.location.x - (45 * screen_factor))) / (screen_size.w / 64))) * screen_factor
		
		# if ship is firing, move laser up screen				
		if(self.firing):
			self.laser.frame.y += 7 * screen_factor
			if(self.laser.frame.y > screen_size.h + 10):
				self.laser.frame.y = (screen_size.h / 20) * 4
				self.laser.alpha = 0
				self.firing = False
				
		# move space monsters
		for i in range(5):
			frame = self.space_monster[i].frame
			
			if(frame.x > screen_size.w - frame.w):
				self.space_monster_move_x[i] = randint(-self.space_monster_max_speed, -1)
			elif(frame.x < 0):
				self.space_monster_move_x[i] = randint(1, self.space_monster_max_speed)
				
			frame.x = frame.x + (self.space_monster_move_x[i] * screen_factor)
			
			# regen space monsters
			if(self.space_monster[i].alpha == 0):
				random_regen = randint(1, 200)
				
				if(random_regen == 1):
					self.space_monster[i].frame.x = -self.space_monster[i].frame.w
					self.space_monster[i].alpha = 1
				elif(random_regen == 200):
					self.space_monster[i].frame.x = screen_size.w
					self.space_monster[i].alpha = 1
			
			# do space monster firing		
			if(self.space_monster_firing[i]):
				self.space_monster_laser[i].frame.y -= 7 * screen_factor
				
				if(self.space_monster_laser[i].frame.y < -self.space_monster_laser[i].frame.h):
					self.space_monster_firing[i] = False
			else:
				if(self.space_monster[i].alpha == 1):
					if(randint(1, self.space_monster_fire_rate) == 1):
						self.space_monster_laser[i].frame = Rect(self.space_monster[i].frame.x + 				(self.space_monster[i].frame.w / 2), self.space_monster[i].frame.y - 15, 6 * screen_factor, 20 * screen_factor)
						self.space_monster_laser[i].alpha = 1
						self.space_monster_firing[i] = True
						sound.play_effect('Laser_6')
		
		# detect players laser to space monster collision		
		for i in range(5):
			# if collision detected and space monster is currently alive (visible)
			if(self.laser.frame.intersects(self.space_monster[i].frame) and self.space_monster[i].alpha == 1):
				# update laser properties
				self.laser.frame.y = (screen_size.h / 20) * 3
				self.laser.alpha = 0
				self.firing = False
				self.space_monster[i].alpha = 0
				
				# update space monster properties
				if(self.space_monster_fire_rate > 22):
					self.space_monster_fire_rate -= 30
				if(self.space_monster_max_speed < 15):
					self.space_monster_max_speed += 1
				
				# add points
				self.score += 2 * (6-i)
				
				# play sound
				sound.play_effect('Explosion_2')
				
		# detect space monster laser to player collision		
		for i in range(5):
			# create a test frame - ship frame is larger than image
			test_frame = Rect(self.ship.frame.x + (self.ship.frame.w / 4), self.ship.frame.y + (self.ship.frame.h / 4),
			                  self.ship.frame.w - (self.ship.frame.w / 2), self.ship.frame.h - (self.ship.frame.h / 2))
			                  
			# if collision detected
			if(self.space_monster_laser[i].frame.intersects(test_frame)):
				sound.play_effect('Explosion_4')
				sleep(5)
				main_scene.switch_scene(Intro)
		
	# draw scene
	def draw(self):
		background(0.2,0,0.1)
		
		tint(0.75,0.2,0.4)
		score = 'Score: {0}'.format(self.score)
		text(score, x=(screen_size.w/2), y=(screen_size.h/20) * 18, font_size=48*screen_factor)
		
		self.layer.draw()
		
	def touch_began(self, touch):
		# set firing and play sound on two finger touch
		if(len(self.touches) == 2 and not(self.firing)):
			sound.play_effect('Laser_1')
			self.firing = True
			self.laser.frame.x = self.ship.frame.x + (self.ship.frame.w / 2) - 3
			self.laser.alpha = 1
				
# multiscene class provides the logic for switching scenes
class MultiScene (Scene):
	def __init__(self, new_scene):
		self.active_scene = new_scene()
		
	def switch_scene(self, new_scene):
		self.active_scene = new_scene()
		self.setup()
		
	def setup(self):
		global screen_size, screen_factor
		screen_size = self.size
		
		# screen_factor is used throughout to ensure
		# correct appearence across devices
		screen_factor = screen_size.h / 1024
		
		self.active_scene.add_layer = self.add_layer
		self.active_scene.touches = self.touches
		self.active_scene.setup()
		
	def draw(self):
		self.active_scene.touches = self.touches
		self.active_scene.update(self.dt)
		self.active_scene.draw()
		
	def touch_began(self, touch):
		self.active_scene.touch_began(touch)
		
	def touch_moved(self, touch):
		self.active_scene.touch_moved(touch)
		
	def touch_ended(self, touch):
		self.active_scene.touch_ended(touch)
		
		
main_scene = MultiScene(Intro)
run(main_scene, orientation=PORTRAIT)
