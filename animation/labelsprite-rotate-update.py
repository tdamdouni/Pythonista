# https://forum.omz-software.com/topic/3312/labelsprite-rotate_by-problem/5

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

# --------------------

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

# --------------------

from scene import *
from math import *

class MyScene(Scene):
	def repeat(self):
		self.rotate_action = Action.sequence(
		Action.rotate_to(self.angles[0], 1, TIMING_EASE_IN_OUT),
		Action.rotate_to(self.angles[1], 1, TIMING_EASE_IN_OUT),
		Action.call(self.repeat), 0)
		self.time_anchor.run_action(self.rotate_action)
		
	def setup(self):
		self.background_color = 'black'
		self.time_anchor = Node(position=(self.size.w/2, 0), parent=self)
		self.timelabel = LabelNode(position=(0, self.size.h/2), text='time')
		self.time_anchor.add_child(self.timelabel)
		self.angles = (pi/8, -pi/8)
		self.rotate_action = Action.sequence(
		Action.rotate_to(self.angles[0], 1, TIMING_EASE_IN_OUT),
		Action.rotate_to(self.angles[1], 1, TIMING_EASE_IN_OUT),
		Action.call(self.repeat), 0)
		self.time_anchor.run_action(self.rotate_action)
		self.toggle = True
		
	def touch_began(self, touch):
		if self.toggle:
			self.angles = (pi/4, -pi/4)
		else:
			self.angles = (pi/8, -pi/8)
		self.toggle = not self.toggle
		
run(MyScene(), PORTRAIT)

# --------------------

from scene import *
from math import *

class MyScene(Scene):
	def setup(self):
		self.background_color = 'black'
		self.timelabel = LabelNode(position=self.size/2, text='time')
		self.add_child(self.timelabel)
		self.ang = -45
		self.delta = 1
	def update(self):
		self.ang = self.ang + self.delta
		if abs(self.ang) > 45:
			self.delta = -self.delta
			self.ang = self.ang + self.delta
		self.timelabel.rotation = math.radians(self.ang)
		r = self.size[1]/2
		x = self.size[0]/2+r*sin(math.radians(-self.ang))
		y = r*cos(math.radians(self.ang))
		self.timelabel.position = (x,y)
		
run(MyScene(), PORTRAIT,frame_interval=1)

# --------------------

self.ang = self.ang + self.delta*cos(radians(2*self.ang)) +.05*self.delta

# --------------------

