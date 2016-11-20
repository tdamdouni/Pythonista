#!python2

# http://2013.globalgamejam.org/sites/default/files/2013/%3Cem%3EEdit%20Game%202013%3C/em%3E%20Dead%20Man/download/dead%20man.zip

# by daniel livingstone for global game jam 2013
# very hacky with all sorts of bad code...
# maybe I'll fix this one day, but don't bet on it...
# art resources will be shared also
# check project home page at 
# http://globalgamejam.org/2013/dead-man
#
# enjoy, but be careful not to drop your iPad
# i am not responsible for any breakages!
import sys
from scene import *
from random import random
from string import *
from sound import *

class MyScene (Scene):
	def setup(self):
		# This will be called before the first frame is drawn.
		# Set up the layers
		self.root_layer = Layer(self.bounds)
		center = self.bounds.center()
		self.player = Layer(Rect(center.x - 24, 64, 48, 64))
		self.grave = Layer(Rect(center.x-32, self.bounds.h-146,64,128))
		self.grave.image = '_Grave'
		self.root_layer.add_layer(self.grave)
		self.heart = Layer(Rect(16,840,128,128))
		self.road1 = Layer(Rect(0,180,self.bounds.w,128))
		self.road1.image = '_Road1'
		self.root_layer.add_layer(self.road1)
		self.road2 = Layer(Rect(0,620,self.bounds.w,128))
		self.road2.image = '_Road1'
		self.root_layer.add_layer(self.road2)
		self.player.image = '_crawl1'
		self.root_layer.add_layer(self.player)
		self.truck = Layer(Rect(self.bounds.w-64, center.y + 140, 128, 96))
		self.truck2 = Layer(Rect(0,200,128,96))
		self.truck.image = '_truck1'
		self.root_layer.add_layer(self.truck)
		self.truck2.image = '_truck1'
		self.truck2.scale_x = -1.0
		self.root_layer.add_layer(self.truck2)	
		self.heart.image = '_BrokenHeart1'
		self.root_layer.add_layer(self.heart)
		self.root_layer.background = Color(0.5,1.0,0.5)
		self.heart.animate('alpha', 0.7, duration=0.1,
						   autoreverse=True, repeat=sys.maxint)
		self.heart.animate('scale_x', 0.8, duration=0.1,
						   autoreverse=True, repeat=sys.maxint)
		set_volume(0.7)
		self.up = True
		load_effect('Drums_01')
		self.dead = True
		self.splash = True
		self.init = False
		self.buried = False
		self.splashStart()
		self.heartStart=self.t
		self.heartTime = 120
		self.heartScale = 1.0

	def heartbeat(self):
		self.player.frame.y = self.player.frame.y + 6
		self.player.scale_x = -1 * self.player.scale_x
		play_effect('Drums_01')

	def splat(self):
		play_effect('Crashing')
		self.player.image = '_CrawlSplat'
		self.dead=True
		self.heart.remove_all_animations()
		self.heart.animate('scale_x', 0.2, duration=2.0)
		self.heart.animate('scale_y',0.2, duration=2.0)
		self.deadText = TextLayer('Rest in Pieces. Oh dear.', 'Baskerville-Bold', 64)
		self.deadText.tint = Color(0.5,0,0)
		self.deadText.frame.center(self.bounds.w/2,400)
		self.root_layer.add_layer(self.deadText)
		self.resetText = TextLayer('touch anywhere to restart', 'Baskerville-Bold', 32)
		self.resetText.frame.center(self.bounds.w/2,200)
		self.resetText.animate('alpha', 0.5, duration=0.2,
						   autoreverse=True, repeat=sys.maxint)
		self.root_layer.add_layer(self.resetText)

	def update(self):
		progress = 1.0 - 0.8 * ((self.t - self.heartStart) / self.heartTime)
		self.heartScale = progress
		#if (math.fmod(self.t-self.heartStart,10) <=0):
		#	play_effect('Coin_2')
		self.heart.scale_y = progress
		self.root_layer.update(self.dt)
		self.truck.frame.x = self.truck.frame.x-1.3
		if (self.truck.frame.x < 0-self.truck.frame.w):
			self.truck.frame.x = self.bounds.w
		self.truck2.frame.x = self.truck2.frame.x+1
		if (self.truck2.frame.x > self.bounds.w):
			self.truck2.frame.x = 0-self.truck2.frame.w
		g = gravity()
#		self.text_layer = TextLayer(str(g.y), 'Futura', 60)
#		self.text_layer.frame.center(self.bounds.center())
		if (self.dead):
			return
		if (self.up  and g.y > 0.7):
			self.heartbeat()
			self.up = False	
		elif (self.up == False and g.y < -0.7 ):
			self.heartbeat()
			self.up = True
		if ( (self.player.frame.intersects(self.truck.frame)) or (self.player.frame.intersects(self.truck2.frame)) ):
			self.splat()
		if (self.t > self.heartStart + self.heartTime):
			self.splat()
		if (self.player.frame.y > self.bounds.h-180):
			self.sixFootUnder()
	
	def sixFootUnder(self):
		play_effect('Powerup_3')
		self.dead = True
		self.buried = True
		self.heart.remove_all_animations()
		self.deadText = TextLayer('Rest in Peace. Huzzah!', 'Baskerville-Bold', 66)
		self.deadText.tint = Color(0.0,0.0,0.5)
		self.deadText.frame.center(self.bounds.w/2,400)
		self.root_layer.add_layer(self.deadText)
		self.resetText = TextLayer('touch anywhere to restart', 'Baskerville-Bold', 32)
		self.resetText.frame.center(self.bounds.w/2,200)
		self.resetText.animate('alpha', 0.5, duration=0.2,
						   autoreverse=True, repeat=sys.maxint)
		self.root_layer.add_layer(self.resetText)
	
			
	def splashStart(self):
		play_effect('Explosion_5')
		title_layer = TextLayer('Dead Man', 'Baskerville-Bold', 100)
		title_layer.frame.center(self.bounds.w/2,self.bounds.h-320)
		self.startTime = self.t
		self.overlay = Layer(self.bounds)
		self.overlay.background = Color(0, 0, 0, 0)
		self.overlay.add_layer(title_layer)
		self.add_layer(self.overlay)
		title_layer.animate('scale_x', 1.3, 0.3, autoreverse=True)
		title_layer.animate('scale_y', 1.3, 0.3, autoreverse=True)
		
	def splashText(self):
		if (self.init == False):
			fontsize = 26
			text_layer1 = TextLayer('You are dead. Almost. Painfully crawl your way to', 'Baskerville-Bold', fontsize)
			text_layer1.frame.center(self.bounds.w/2,self.bounds.h-380)
			self.overlay.add_layer(text_layer1)
			text_layer1 = TextLayer('your grave, before your heart gives out, by tilting', 'Baskerville-Bold', fontsize)
			text_layer1.frame.center(self.bounds.w/2,self.bounds.h-410)
			self.overlay.add_layer(text_layer1)
			text_layer1 = TextLayer('the pad up and down. Try not to get squashed on the', 'Baskerville-Bold', fontsize)
			text_layer1.frame.center(self.bounds.w/2,self.bounds.h-440)
			self.overlay.add_layer(text_layer1)
			text_layer1 = TextLayer('way, else your soul will never rest in peace.', 'Baskerville-Bold', fontsize)
			text_layer1.frame.center(self.bounds.w/2,self.bounds.h-470)
			self.overlay.add_layer(text_layer1)
			text_layer1 = TextLayer('Plus your family would never live it down.', 'Baskerville-Bold', fontsize)
			text_layer1.frame.center(self.bounds.w/2,self.bounds.h-520)
			self.overlay.add_layer(text_layer1)
			text_layer1 = TextLayer('touch anywhere to start', 'Baskerville-Bold', 32)
			text_layer1.frame.center(self.bounds.w/2,200)
			text_layer1.animate('alpha', 0.5, duration=0.2,
						   autoreverse=True, repeat=sys.maxint)
			self.overlay.add_layer(text_layer1)
			self.init = True 
		
	def splashScreen(self):
		self.overlay.draw()
		if (self.t > self.startTime + 1.0):
			self.splashText()
		#self.touch_disabled = True
		#self.root_layer.animate('scale_x', 0.0, delay=2.0,
		#						curve=curve_ease_back_in)
		#self.root_layer.animate('scale_y', 0.0, delay=2.0,
		#						curve=curve_ease_back_in,
		#						completion=self.new_game)
		
	def draw(self):
		# Update and draw our root layer. For a layer-based scene, this
		# is usually all you have to do in the draw method.
		self.update()
		background(0, 0, 0)
		#image('_Road1',100,100,128,128)
		if (self.splash):
			self.splashScreen()
		else:
			self.root_layer.draw()
#		self.text_layer.draw()
	
	def touch_began(self, touch):
		# Animate the layer to the location of the touch:
#		x, y = touch.location.x, touch.location.y
#		new_frame = Rect(x - 64, y - 64, 48, 64)
#		self.player.animate('frame', new_frame, 1.0, curve=curve_bounce_out)
		if (self.splash):
			self.splash=False
			self.dead = False
			play_effect('Ding_3')
			self.overlay.remove_layer()
			self.heartStart = self.t
		elif (self.dead):
			center = self.bounds.center()
			self.player.frame = Rect(center.x - 24, 64, 48, 64)
			self.dead = False 
			self.buried = False
			self.deadText.remove_layer()
			self.resetText.remove_layer()
			self.player.image = '_crawl1'
			self.heart.remove_all_animations()
			self.heart.scale_y = 1.0
			self.heart.scale_x = 1.0
			self.heart.alpha = 1.0
			self.heartStart = self.t
			self.heart.animate('alpha', 0.7, duration=0.1,
						   autoreverse=True, repeat=sys.maxint)
			self.heart.animate('scale_x', 0.8, duration=0.1,
						   autoreverse=True, repeat=sys.maxint)

	def touch_moved(self, touch):
		pass
	
	def touch_ended(self, touch):
		pass

run(MyScene(),PORTRAIT)

