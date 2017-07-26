# https://forum.omz-software.com/topic/3312/labelsprite-rotate_by-problem/4

from itertools import cycle
from scene import *
from math import *

class MyScene(Scene):

	def setup(self):
		self.background_color = 'black'
		self.time_anchor = Node(position=(self.size.w/2, 0), parent=self)
		self.timelabel = LabelNode(position=(0, self.size.h/2), text='time')
		self.time_anchor.add_child(self.timelabel)
		self.angles = cycle([pi/4, -pi/4])
		rotate_action = Action.repeat(Action.rotate_to(self.angles.next(), 1, TIMING_EASE_IN_OUT), 0)
		self.time_anchor.run_action(rotate_action)
		
run(MyScene(), PORTRAIT)

