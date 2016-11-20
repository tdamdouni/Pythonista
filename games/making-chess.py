# https://forum.omz-software.com/topic/3622/making-chess-any-tips

from scene import *
from Chessboard import Chessboardd
class game(Scene):
	def __init__(self):
		Scene.__init__(self)
		
	def setup(self):
		self.r = Chessboardd(self.bounds.center(), Size(700, 700))
		self.kingw = LabelNode(u"\N{WHITE CHESS KING}", font=('Helvetica', 100), position=(468 + 88,75), parent=self)
	def draw(self):
		background(0,0,0)
		self.r.draw()
		
	def touch_ended(self, Touch):
		if Touch.location.x < self.kingw.frame.x and Touch.location.x > self.kingw.frame.x - 88 and Touch.location.y < self.kingw.frame.y + 90 and Touch.location.y > self.kingw.frame.y:
			self.kingw.run_action(Action.move_by(-88,0))
		if Touch.location.x > self.kingw.frame.x + 70 and Touch.location.x < self.kingw.frame.x + 50 + 125 and Touch.location.y < self.kingw.frame.y + 90 and Touch.location.y > self.kingw.frame.y:
			self.kingw.run_action(Action.move_by(88,0))
		if Touch.location.y < self.kingw.frame.y and Touch.location.y > self.kingw.frame.y - 88 and Touch.location.x > self.kingw.frame.x and Touch.location.x < self.kingw.frame.x + 88:
			self.kingw.run_action(Action.move_by(0,-88))
		if Touch.location.y > self.kingw.frame.y + 100 and Touch.location.y < self.kingw.frame.y + 100 + 110 and Touch.location.x > self.kingw.frame.x and Touch.location.x < self.kingw.frame.x + 88:
			self.kingw.run_action(Action.move_by(0,88))
		if Touch.location.x < self.kingw.frame.x and Touch.location.x > self.kingw.frame.x - 90 and Touch.location.y > self.kingw.frame.y + 88 and Touch.location.y < self.kingw.frame.y + 88 + 88:
			self.kingw.run_action(Action.move_by(-88,88))
		if Touch.location.x > self.kingw.frame.x + 88 and Touch.location.x < self.kingw.frame.x + 88 + 88 and Touch.location.y > self.kingw.frame.y + 88 and Touch.location.y < self.kingw.frame.y + 88 + 88:
			self.kingw.run_action(Action.move_by(88,88))
		if Touch.location.x < self.kingw.frame.x and Touch.location.x > self.kingw.frame.x - 88 and Touch.location.y < self.kingw.frame.y and Touch.location.y > self.kingw.frame.y - 88:
			self.kingw.run_action(Action.move_by(-88,-88))
		if Touch.location.x > self.kingw.frame.x + 88 and Touch.location.x < self.kingw.frame.x + 88 + 88 and Touch.location.y < self.kingw.frame.y and Touch.location.y > self.kingw.frame.y - 88:
			self.kingw.run_action(Action.move_by(88,-88))
run(game())
# --------------------
from scene import *
class Chessboardd:
	def __init__(self, position, size):
		self.position = position
		self.size = size
	def draw(self):
		fill(1,0,0)
		for x in range(8):
			for y in range(8):
				black = (x + y) % 2 == 0 # true if checkerboard square should be black
				if black:
					fill(.66, .46, .25)
				else:
					fill(1.0, .7, .38)
				rect(self.position.x + self.size.w*(x/8.0) - self.size.w/2.0, self.position.y + self.size.h*(y/8.0) - self.size.h/2.0, self.size.w/8.0, self.size.h/8.0)
				
# --------------------

