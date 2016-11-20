# https://forum.omz-software.com/topic/3660/how-to-virtual-d-pad-that-moves-a-sprite-only-when-screen-touched/3

from scene import *

class MyScene (Scene):
	def setup(self):
		self.background_color = 'midnightblue'
		self.ship = SpriteNode('spc:PlayerShip1Orange',
		position=self.size/2,
		parent=self)
		self.sp = self.size.y - self.ship.size.y
		
	def touch_began(self, touch):
		if touch.location.x < 100:
			self.ship.run_action(
			Action.move_to(self.ship.position[0], self.sp, 2, TIMING_EASE_IN_OUT), 'move_action_key')
			
	def touch_ended(self, touch):
		if touch.location.x < 100:
			self.ship.remove_action('move_action_key')
			
run(MyScene(), PORTRAIT)

