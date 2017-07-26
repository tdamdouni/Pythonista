# coding: utf-8

# https://gist.github.com/chriswilson1982/2dae9cf90ed4d71c2bb8b2c3158e3997

# An experiment in drawing line_segments from touches in Pythonista using the scene module.

# https://forum.omz-software.com/topic/3184/understanding-sprite-coordinate-systems/2

from scene import *
import sound
import random
import math
import ui

# Maths functions

def angle(a, b):
		x1, y1=a
		x2, y2=b
		def cartToPol(x,y):
			radius = math.sqrt(x**2 + y**2)
			theta = math.atan2(y,x)
			theta += math.pi
			return radius,theta
		return cartToPol(x2-x1,y2-y1)[1]

def distance(a, b):
	return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def is_between(a, c, b, spd):
	try:
		return distance(a, c) + distance(c, b) <= distance(a, b) + 0.1 * spd
	except:
		pass

# Screen setup

screen_w = int(get_screen_size()[0])
screen_h = int(get_screen_size()[1])

marker = ui.Path().oval(0, 0, 10, 10)
marker.fill()
marker.close()

# Actions

A = Action
action_ball_bounce = A.sequence(A.group(A.scale_y_to(1.2, 0.1), A.scale_x_to(0.8, 0.1)), A.group(A.scale_y_to(0.9, 0.1), A.scale_x_to(1.1, 0.1)), A.group(A.scale_y_to(1.1, 0.2), A.scale_x_to(0.9, 0.2)), A.group(A.scale_y_to(1, 0.2), A.scale_x_to(1, 0.2)))
action_line_bounce = A.sequence(A.scale_y_to(1.5, 0.1), A.scale_y_to(1, 0.4))


# Game class
class Game (Scene):
	def setup(self):
		self.background_color = "#b1ffb1"
		self.count = 0
		self.a = None
		self.b = None
		self.pending_mark_a = None
		self.prev_mark_a = None
		self.mark_a = None
		self.mark_b = None
		self.line_segment = None
		self.temp_line = None
		self.cross_point = None
		self.invalid_draw = False
		
		boundary_path = ui.Path().rounded_rect(0, 0, screen_w - 64, screen_h - 160, 4)
		boundary_path.line_width = 4
		boundary_path.stroke()
		self.boundary = ShapeNode(boundary_path, position = (screen_w / 2, screen_h / 2 + 48), stroke_color = '#000000')
		self.add_child(self.boundary)
		
		self.ball = Ball(2)
		self.add_child(self.ball)
		
		self.lead_list = []
		for x in range(32):
			self.lead = Lead(x + 1)
			self.add_child(self.lead)
			self.lead_list.append(self.lead)
		
		text = LabelNode("Drag to create a wall!", position = (screen_w/2, screen_h - 100), font = ('Helvetica Neue', 20), color = "#000000")
		self.add_child(text)
		
		
	def did_change_size(self):
		pass
	
	
	def update(self):
		self.ball.move()
		for item in self.lead_list:
			item.move()
		self.hit_test()
	
	
	def touch_began(self, touch):
		if touch.location not in self.boundary.bbox:
			self.invalid_draw = True
			return
		self.invalid_draw = False
		self.b = None
		self.a = touch.location
		
		self.prev_mark_a = self.mark_a
		
		self.pending_mark_a = ShapeNode(marker, position = self.a, color = "#00ff00", size = (30,30))
		self.pending_mark_a.z_position = 1
		self.add_child(self.pending_mark_a)
	
	
	def touch_moved(self, touch):
		if touch.location not in self.boundary.bbox:
			if not self.cross_point:
				self.cross_point = touch.location
			return
		if self.invalid_draw:
			return
		self.pending_mark_a.run_action(A.remove()) 
		try:
			self.temp_line.run_action(A.remove())
		except:
			pass
		
		line_path = ui.Path().rect(0, 0, distance(self.a, touch.location), 4)
		line_path.fill()
		line_path.close()
		
		self.temp_line = ShapeNode(line_path, position = (self.a + touch.location) / 2, fill_color = "#929292")
		self.temp_line.rotation = angle(self.a, touch.location)
		self.temp_line.z_position = 0.3
		self.add_child(self.temp_line)
	
	
	def touch_ended(self, touch):
		if self.invalid_draw:
			return
		try:
			self.temp_line.run_action(A.remove())
		except:
			pass
		
		for item in (self.prev_mark_a, self.pending_mark_a, self.mark_b, self.temp_line):
			try:
				item.run_action(A.remove())
			except:
				pass
		try:
			self.line_segment.run_action(A.sequence(A.group(A.scale_x_to(0, 0.1), A.fade_to(0, 0.1)), A.remove()))
		except:
			pass
		
		self.mark_a = SpriteNode(texture = Texture('shp:Circle'), position = self.a, color = "#000000", size = (10,10))
		self.mark_a.z_position = 0.39
		self.add_child(self.mark_a)
		
		self.b = touch.location if touch.location in self.boundary.bbox else self.cross_point
		self.mark_b = SpriteNode(texture = Texture('shp:Circle'), position = self.b, color = "#000000", size = (10,10))
		self.mark_b.z_position = 0.39
		self.add_child(self.mark_b)
		
		length = distance(self.a, self.b) if touch.location in self.boundary.bbox else distance(self.a, self.cross_point)
		
		line_path = ui.Path().rect(0, 0, length, 4)
		line_path.fill()
		line_path.close()
		
		self.line_segment = ShapeNode(line_path, position = (self.a + self.b) / 2 if touch.location in self.boundary.bbox else (self.a + self.cross_point) / 2, fill_color = "#000000")
		self.line_segment.z_position = 0.38
		
		self.line_segment.rotation = angle(self.a, self.b) if touch.location in self.boundary.bbox else angle(self.a, self.cross_point)
		self.add_child(self.line_segment)
		
		self.cross_point = None
		sound.play_effect('digital:Zap1')
		
	# Tests if ball colliding with boundary or line
	def hit_test(self):
		for item in self.lead_list:
			try:
				if is_between(self.mark_a.position, item.position, self.mark_b.position, self.ball.spd):
					self.ball.rotation = self.line_segment.rotation + math.pi / 2
					self.ball.bounce(self.line_segment.rotation)
					self.line_segment.run_action(action_line_bounce)
					return
			except:
				pass
			
			
			rot = math.pi / 2.0
			if item.position[0] < 32 or item.position[0] > self.size.w - 32:
				self.ball.rotation = 2 * rot
				self.ball.bounce(rot)
			
			elif item.position[1] < 128 or item.position[1] > self.size.h - 32:
				self.ball.rotation = rot
				self.ball.bounce(2 * rot)
	
# Ball class
class Ball (SpriteNode):
	def __init__(self, spd = 2):
		self.spd = spd
		self.direction = random.random() * 2 * math.pi
		self.position = (screen_w / 2, screen_h / 2)
		self.texture = Texture('shp:Circle')
		self.color = 'blue'
		self.size = (24, 24)
		self.z_position = 1
		
	def move(self):
		dx = math.cos(self.direction)
		dy = math.sin(self.direction)
		self.position += (dx * self.spd, dy * self.spd)
	
	def leading_edge(self):
		return self.position + (math.cos(self.direction) * self.size[0] / 2, math.sin(self.direction) * self.size[1] / 2)
	
	def bounce(self, surface_direction):
		self.direction = self.direction - 2 * (self.direction - surface_direction)
		self.run_action(action_ball_bounce)
		sound.play_effect('digital:PepSound3')


# Lead class (ball edge collision detection)
class Lead (Node):
	def __init__(self, index):
		self.index = index
		self.size = (1, 1)
		self.alpha = 0
	
	def move(self):
		self.position = self.parent.ball.position + (math.cos(math.pi / 16 * self.index) * self.parent.ball.size[0] / 2.8, math.sin(math.pi / 16 * self.index) * self.parent.ball.size[1] / 2.8)
		

# Run game
if __name__ == '__main__':
	run(Game(), show_fps=False)
