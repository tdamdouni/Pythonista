# coding: utf-8

# https://forum.omz-software.com/topic/2564/help-with-actions-for-spritenodes

from scene import *

class MyScene (Scene):
	def setup(self):
		self.background_color = 'midnightblue'
		self.ship = SpriteNode('spc:PlayerShip1Orange')
		self.ship.position = self.size/2
		self.add_child(self.ship)
		self.badGuy = SpriteNode('spc:EnemyBlack4')
		self.bx,self. by = self.size
		self.by -= 50
		self.bx += 50
		self.badGuy.position = (self.bx, self.by)
		self.add_child(self.badGuy)
		
	def update(self):
		x,y,z = gravity()
		pos = self.ship.position
		pos += (x * 15, y * 15)
		pos.x = max(0, min(self.size.w, pos.x))
		pos.y = max(0, min(self.size.h, pos.y))
		self.ship.position = pos
		
	def resetBad(self):
		self.badGuy.position = (self.bx, self.by)
		
	def touch_began(self, touch):
		resetBadGuy = Action.call(self.resetBad())
		laser = SpriteNode('spc:LaserBlue9', position=self.ship.position, z_position=-1, parent=self)
		laser.run_action(Action.sequence(Action.move_by(0,1000), Action.remove()))
		self.badGuy.run_action(Action.repeat(Action.sequence(Action.move_by(-818, 0, 5), resetBad), -1))
		print self.badGuy.position.x
		#self.badGuy.position = (self.bx, self.by)
		
		
		
run(MyScene(), PORTRAIT)

#==============================

		#pos.x = max(0, min(self.size.w, pos.x))
		#pos.y = max(0, min(self.size.h, pos.y))
	pos.x %= self.size.w
	pos.y %= self.size.h
	
#==============================

def update(self):
	x,y,z = gravity()
	pos = self.ship.position
	pos += (x * 15, y * 15)
	pos.x = max(0, min(self.size.w, pos.x))
	pos.y = max(0, min(self.size.h, pos.y))
	self.ship.position = pos
	
def resetBad(self):
	self.badGuy.position = (self.bx, self.by)
	
def touch_began(self, touch):
	resetBadGuy = Action.call(self.resetBad)
	laser = SpriteNode('spc:LaserBlue9', position=self.ship.position, z_position=-1, parent=self)
	laser.run_action(Action.sequence(Action.move_by(0,1000), Action.remove()))
	self.badGuy.run_action(Action.repeat(Action.sequence(Action.move_by(-818, 0, 5), self.resetBad), -1))
	print self.badGuy.position.x
	#self.badGuy.position = (self.bx, self.by)
	
#==============================

def setup(self):
	self.background_color = 'midnightblue'
	self.ship = SpriteNode('spc:PlayerShip1Orange')
	self.ship.position = self.size/2
	self.add_child(self.ship)
	self.badGuy = SpriteNode('spc:EnemyBlack4')
	self.bx,self. by = self.size
	self.by -= 50
	self.bx += 50
	self.badGuy.position = (self.bx, self.by)
	self.add_child(self.badGuy)
	self.bad_guy()
	
def update(self):
	x,y,z = gravity()
	pos = self.ship.position
	pos += (x * 15, y * 15)
	pos.x = max(0, min(self.size.w, pos.x))
	pos.y = max(0, min(self.size.h, pos.y))
	self.ship.position = pos
	
def touch_began(self, touch):
	laser = SpriteNode('spc:LaserBlue9', position=self.ship.position, z_position=-1, parent=self)
	laser.run_action(Action.sequence(Action.move_by(0,1000), Action.remove()))
	
#==============================

	for child in self.children:
		if child not in (self.ship, self.badGuy) and child.frame in self.badGuy.frame:
			exit("It's a hit!")

