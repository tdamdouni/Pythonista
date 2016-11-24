# https://forum.omz-software.com/topic/3684/basic-touch-question

from scene import *
class MyScene(Scene):

	def setup(self):
		self.background_color = 'midnightblue'
		self.ship = SpriteNode('spc:PlayerShip1Orange')
		self.ship.position = self.size / 2
		self.add_child(self.ship)
		
	def update(self):
		fill('green')
		ellipse(200, 100, 100, 100)
		
	def touch_began(self, touch):
		x,y = touch.location
		if x>200 and x<300 and y>100 and y<200:
			move_action = Action.move_by(10, 10, 0.7, TIMING_SINODIAL)
			self.ship.run_action(move_action)
if __name__ == '__main__':
	run(MyScene(), LANDSCAPE, show_fps=True)

