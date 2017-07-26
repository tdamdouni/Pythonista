
# coding: utf-8

# https://forum.omz-software.com/topic/3620/moving-a-node-help

from scene import *

class game(Scene):
	def __init__(self):
		Scene.__init__(self)
	def setup(self):
		self.test = LabelNode("memes", font=('Helvetica', 100), position=  (500,500), parent=self)
		pass
	def draw(self):
		background(0,0,0)
		
	def touch_ended(self, Touch):
		self.test.run_action(Action.move_to(Touch.location.x,Touch.location.y))
		
run(game())

