# https://gist.github.com/balachandrana/d2bbb4ec151bd706e87f1f38c90181f6

import scene
import copy
import math
import ui

class Paddle(scene.ShapeNode):
	def __init__(self, x, y, parent=None):
		path = ui.Path.rect(0,0, 40, 200)
		super(Paddle, self).__init__(path, position=(x, y), fill_color='green', parent=parent)
		self.touch = None
		
	def touch_began(self, touch):
		if touch.location in (self.frame):
			if not self.touch:
				self.touch = copy.copy(touch)
				
	def touch_moved(self, touch):
		if self.touch and touch.touch_id == self.touch.touch_id:
			dx = touch.location.y - self.touch.location.y
			if abs(dx*1.0) > 5:
				self.touch.location.y = touch.location.y
				self.position = (self.position[0], touch.location.y)
				
	def touch_ended(self, touch):
		if self.touch and touch.touch_id == self.touch.touch_id:
			self.touch = None
			
			
class Ball(scene.ShapeNode):
	def __init__(self, x, y, parent=None):
		path = ui.Path.oval(0,0, 10, 10)
		super(Ball, self).__init__(path, position=(x, y), fill_color='red', parent=parent)
		self.dx, self.dy = 5, 0
		
	def update(self):
		self.position = (self.position[0] + self.dx,
		self.position[1]+self.dy)
		if (self.position[1] > self.parent.bounds.h) or (self.position[1] < 0) :
			self.dy = -self.dy
			return
		if (self.frame.x > self.parent.bounds.w):
			self.dx, self.dy = 5, 0
			self.position = (400, 300)
			self.parent.score_left.increment()
			return
		if (self.frame.x < 0):
			self.dx, self.dy =  -5, 0
			self.position = (400, 300)
			self.parent.score_right.increment()
			return
		if self.frame.intersects(self.parent.paddle_left.frame):
			self.dx = -self.dx
			h = self.parent.paddle_left.frame.h/2
			self.dy += (self.frame.y+self.frame.h/2 - (self.parent.paddle_left.frame.y+h))*1.0/h*5
		if self.frame.intersects(self.parent.paddle_right.frame):
			self.dx = -self.dx
			h = self.parent.paddle_right.frame.h/2
			self.dy += (self.frame.y+self.frame.h/2 - (self.parent.paddle_right.frame.y+h))*1.0/h*5
			
			
class Score(object):
	def __init__(self, x, y, parent=None):
		self.value = 0
		self.label = scene.LabelNode(
		"{}".format(self.value),
		position=(x, y),
		font=('Helvetica', 40),
		parent=parent)
		
	def increment(self):
		self.value += 1
		self.label.text = "{}".format(self.value)
		
	def reset(self):
		self.value = 0
		self.label.text = "{}".format(self.value)
		
class Pong(scene.Scene):
	def setup(self):
		self.paddle_left = Paddle(50, self.size[1]/2.0, parent=self)
		self.paddle_right = Paddle(self.size[0]-50, self.size[1]/2.0, parent=self)
		self.ball = Ball(self.size[0]/2.0, self.size[1]/2.0, parent=self)
		self.score_left = Score(self.size[0]*.25, 25, parent=self)
		self.score_right = Score(self.size[0]*.75, 25, parent=self)
		
	def update(self):
		self.ball.update()
		
	def touch_began(self, touch):
		self.paddle_left.touch_began(touch)
		self.paddle_right.touch_began(touch)
		
	def touch_moved(self, touch):
		self.paddle_left.touch_moved(touch)
		self.paddle_right.touch_moved(touch)
		
	def touch_ended(self, touch):
		self.paddle_left.touch_ended(touch)
		self.paddle_right.touch_ended(touch)
		
scene.run(Pong(), show_fps=True)

