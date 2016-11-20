# https://forum.omz-software.com/topic/3312/labelsprite-rotate_by-problem

from scene import *
from math import *

class MyScene(Scene):

	def setup(self):
		self.background_color = 'black'
		self.anchor_point = (0.5, 0.0)
		self.timelabel = LabelNode(position=self.size / 2, text='time')
		self.add_child(self.timelabel)
		self.timelabel.rotation = -pi / 8.0
		self.run_action(Action.repeat(Action.sequence(Action.rotate_by(pi / 4.0, 1, TIMING_EASE_IN_OUT), Action.rotate_by(-pi / 4.0, 1, TIMING_EASE_IN_OUT), 0), 0))
		
run(MyScene(), PORTRAIT)

# --------------------

# @omz

from scene import *
from math import *

class MyScene(Scene):

	def setup(self):
		self.background_color = 'black'
		self.time_anchor = Node(position=(self.size.w/2, 0), parent=self)
		self.timelabel = LabelNode(position=(0, self.size.h/2), text='time')
		self.time_anchor.add_child(self.timelabel)
		rotate_action = Action.repeat(Action.sequence(Action.rotate_to(pi / 4.0, 1, TIMING_EASE_IN_OUT), Action.rotate_to(-pi / 4.0, 1, TIMING_EASE_IN_OUT), 0), 0)
		self.time_anchor.run_action(rotate_action)
		
run(MyScene(), PORTRAIT)

