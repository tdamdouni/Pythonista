# https://gist.github.com/Uberi/4040487

from scene import *
import sound

class MyScene (Scene):
	def setup(self):
		# This will be called before the first frame is drawn.
		
		self.root_layer = Layer(self.bounds)
		
		self.bullets = {}
		
		#wip
		tint1 = Color(0.8, 0.9, 1)
		tint2 = Color(1, 0.9, 0.8)
		tint3 = Color(0.85, 1, 0.85)
		
		self.player1 = self.Player(self)
		self.player1.move(self.bounds.w / 2, 96)
		self.player1.layer.tint = tint1 #wip
		
		self.player2 = self.Player(self)
		self.player2.move(self.bounds.w / 2, self.bounds.h - 96)
		self.player2.layer.scale_y = -1
		self.player2.layer.tint = tint2 #wip
		
		self.enemy = self.Player(self)
		self.enemy.move(self.bounds.w / 2, self.bounds.h / 2)
		self.enemy.layer.tint = tint3
		
		self.movepad1 = self.Movepad(self, self.player1)
		self.movepad1.move(96, 96)
		self.firepad1 = self.Firepad(self, self.player1)
		self.firepad1.move(self.bounds.w - 96, 96)
		self.movepad1.layer.tint, self.firepad1.layer.tint = tint1, tint1 #wip
		
		self.movepad2 = self.Movepad(self, self.player2)
		self.movepad2.move(self.bounds.w - 96, self.bounds.h - 96)
		self.firepad2 = self.Firepad(self, self.player2)
		self.firepad2.move(96, self.bounds.h - 96)
		self.movepad2.layer.tint, self.firepad2.layer.tint = tint2, tint2 #wip
	
	def draw(self):
		# Update and draw our root layer. For a layer-based scene, this
		# is usually all you have to do in the draw method.
		background(0, 0, 0)
		
		self.movepad1.step(self.dt, self, self.touches)
		self.firepad1.step(self.dt, self, self.touches)
		
		self.movepad2.step(self.dt, self, self.touches)
		self.firepad2.step(self.dt, self, self.touches)
		
		for bullet in self.bullets.keys():
			bullet.update(self.dt, self)
		
		self.root_layer.update(self.dt)
		self.root_layer.draw()
	
	class Movepad:
		def __init__(self, scene, player, rest = 0.4, speed = 300):
			self.player = player
			self.rest = rest
			self.speed = speed
			
			self.layer = Layer(Rect(0, 0, 192, 192))
			#self.layer.background = Color(0.80, 0.80, 0.80, 0.5)
			self.layer.image = 'Typicons192_Move'
			scene.root_layer.add_layer(self.layer)
		
		def move(self, x, y):
			self.layer.frame.center(x, y)
		
		def step(self, dt, scene, touches):
			frame = self.layer.frame
			for touch in touches.values():
				if touch.location in frame:
					self.update(dt, scene, touch.location)
		
		def update(self, dt, scene, location):
			pad = self.layer.frame
			
			movement = self.speed * dt
			if location.x < pad.x + pad.w * self.rest:
				self.player.translate(scene, -movement, 0)
			elif location.x > pad.x + pad.w * (1 - self.rest):
				self.player.translate(scene, movement, 0)
			if location.y < pad.y + pad.h * self.rest:
				self.player.translate(scene, 0, -movement)
			elif location.y > pad.y + pad.h * (1 - self.rest):
				self.player.translate(scene, 0, movement)
			# wip: enemy movement here
	
	class Firepad:
		def __init__(self, scene, player, rest = 0.2):
			self.player = player
			self.rest = rest
			self.cooldown = 0
			
			self.layer = Layer(Rect(0, 0, 192, 192))
			#self.layer.background = Color(0.80, 0.80, 0.80, 0.5)
			self.layer.image = 'Typicons192_Relocate'
			scene.root_layer.add_layer(self.layer)
		
		def move(self, x, y):
			self.layer.frame.center(x, y)
		
		def step(self, dt, scene, touches):
			frame = self.layer.frame
			for touch in touches.values():
				if touch.location in frame:
					self.update(dt, scene, touch.location)
		
		def update(self, dt, scene, location):
			self.cooldown -= dt
			if self.cooldown >= 0:
				return
			self.cooldown = 0.5
			
			frame = self.layer.frame
			center = frame.center()
			x, y = location.x - center.x, location.y - center.y
			distance = location.distance(center)
			if distance < frame.w * 0.5 * self.rest: # insignificant distance
				return
			direction = Point(x / distance, y / distance)
			
			start = self.player.layer.frame.center()
			
			self.player.shoot(scene, start, direction)
	
	class Player:
		def __init__(self, scene):
			self.health = 12
			self.images = {12: 'Clock_12',
			               11: 'Clock_11',
			               10: 'Clock_10',
			               9: 'Clock_9',
			               8: 'Clock_8',
			               7: 'Clock_7',
			               6: 'Clock_6',
			               5: 'Clock_5',
			               4: 'Clock_4',
			               3: 'Clock_3',
			               2: 'Clock_2',
			               1: 'Clock_1'}
			
			self.layer = Layer(Rect(0, 0, 96, 96))
			self.layer.image = self.images[self.health]
			scene.root_layer.add_layer(self.layer)
			
			sound.load_effect('Clank')
		
		def move(self, x, y):
			self.layer.frame.center(x, y)
		
		def translate(self, scene, x, y):
			if self.health <= 0:
				return
			frame = self.layer.frame
			if Rect(frame.x + x, frame.y + y, frame.w, frame.h) in scene.bounds:
				frame.x += x
				frame.y += y
		
		def shoot(self, scene, start, direction):
			if self.health <= 0:
				return
			layer = Layer(Rect(0, 0, 48, 48))
			layer.image = 'Typicons48_Cog'
			scene.root_layer.add_layer(layer)
			
			start = Point(start.x + direction.x * 60, start.y + direction.y * 60)
			bullet = scene.Bullet(start, layer, direction)
			bullet.layer.tint = self.layer.tint #wip
			scene.bullets[bullet] = True
			
			sound.play_effect('Clank')
		
		def hit(self):
			self.health -= 1
			if self.health <= 0:
				self.layer.image = 'Skull'
				if self.health == 0:
					sound.play_effect('Explosion_5')
				return
			
			self.layer.image = self.images[self.health]
			sound.play_effect('Hit_2')
	
	class Bullet:
		def __init__(self, start, layer, direction):
			self.start = start
			self.layer = layer
			self.direction = direction
			self.lifetime = 0
			layer.frame.center(start)
		
		def update(self, dt, scene):
			self.lifetime += dt
			if self.lifetime > 1:
				self.remove(scene)
				return
			
			movement = 500 * dt
			self.layer.frame.x += self.direction.x * movement
			self.layer.frame.y += self.direction.y * movement
			
			radius = 55
			if self.layer.frame.center().distance(scene.player1.layer.frame.center()) < radius:
				scene.player1.hit()
				self.remove(scene)
			if self.layer.frame.center().distance(scene.player2.layer.frame.center()) < radius:
				scene.player2.hit()
				self.remove(scene)
			if self.layer.frame.center().distance(scene.enemy.layer.frame.center()) < radius:
				scene.enemy.hit()
				self.remove(scene)
		
		def remove(self, scene):
			self.layer.remove_layer()
			del scene.bullets[self]

run(MyScene())

