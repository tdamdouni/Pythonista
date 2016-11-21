# https://forum.omz-software.com/topic/3660/how-to-virtual-d-pad-that-moves-a-sprite-only-when-screen-touched/2

from scene import *
import sound
# Global variable that will be changed when you touch the screen.
sp = 0

class MyScene (Scene):
	def setup(self):
		self.background_color = 'midnightblue'
		self.ship = SpriteNode('spc:PlayerShip1Orange')
		self.ship.position = self.size / 2
		self.add_child(self.ship)
		
	def touch_began(self, touch):
		global sp
		if touch.location.x < 100:
			# when the screen is touched then the global variable changes to 1 and should update the movement of the ship in update()... but ship movement does not change.
			sp = 1
			
	def touch_ended(self, touch):
		global sp
		if touch.location.x < 100:
			# i was hoping that once touch_began() started moving ship, that touch_ended() would stop movement so that it works like a simple directional pad.
			sp = 0
			
	def update(self):
		global sp
		x, y = self.ship.position
		'''pos += x + sp, y + sp'''
		#this is just a test to see if touch would change the global variable "sp" and update accordingly. If i change it on line 4 it will update and move the ship. I dont know how to alter sp on the fly to move ship with touch until i stop touching the screen. like a controler moving mario or something.
		y += sp
		# Don't allow the ship to move beyond the screen bounds:
		x = max(0, min(self.size.w, x))
		y = max(0, min(self.size.h, y))
		self.ship.position = (x, y)
		
run(MyScene(), PORTRAIT)

