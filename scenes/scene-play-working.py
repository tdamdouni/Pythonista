# https://forum.omz-software.com/topic/3684/basic-touch-question

from scene import *
class MyScene(Scene):

	def setup(self):
		self.background_color = 'midnightblue'
		self.ship = SpriteNode('spc:PlayerShip1Orange')
		self.ship.position = self.size / 2
		self.dx=100
		self.dy=100
		self.ship.speed = 0
		self.add_child(self.ship)
		
	def update(self):
		fill('green')
		ellipse(200, 100, 100, 100)
		x,y = self.ship.position
		self.ship.position = (x+self.dx*self.dt*self.ship.speed, y+self.dy*self.dt*self.ship.speed)
		
	def touch_began(self, touch):
		x,y = touch.location
		if x>200 and x<300 and y>100 and y<200:
			self.touch_id = touch.touch_id
			self.ship.speed = 1
			
	def touch_ended(self, touch):
		x,y = touch.location
		if self.touch_id == touch.touch_id:
			self.touch_id = None
			self.ship.speed = 0
			
if __name__ == '__main__':
	run(MyScene(), LANDSCAPE, show_fps=True)

