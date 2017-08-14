# https://forum.omz-software.com/topic/4168/analog-clock-example-to-ui-example-help

'''
A simple analog clock made of ShapeNodes.
'''
import ui
from scene import *
from math import pi, sin, cos
from datetime import datetime

class Clock2(ui.View):
	def __init__(self):
		self.width = 600
		self.height = 600
		self.hands = [(),(),()]
		self.update_interval = 1
		
	def update(self):
		self.set_needs_display()
		#print('update')
		
	def draw(self):
		r = min(self.width, self.height)/2 * 0.9
		
		circle = ui.Path.oval(0, 0, r*2, r*2)
		circle.line_width = 6
		
		shadow = ('black', 0, 0, 15)
		ui.set_shadow(*shadow)
		ui.set_color('silver')
		#self.face = ShapeNode(circle, 'white', 'silver', shadow=shadow)
		circle.fill()
		circle.stroke()
		
		for i in range(12):
			label = LabelNode(str(i+1), font=('HelveticaNeue-UltraLight', 0.2*r))
			label.color = 'black'
			a = 2 * pi * (i+1)/12.0
			#label.position = sin(a)*(r*0.85), cos(a)*(r*0.85)
			label.position = sin(a)*(r*0.85), cos(a)*(r*0.85)
			#print(label.position)
			ui.draw_string(str(i+1), rect=(r+ label.position[0], r +label.position[1], 0, 0), font=('<system>', 18), color='black', alignment=ui.ALIGN_CENTER, line_break_mode=ui.LB_WORD_WRAP)
			
		#self.hands = []
		#hand_attrs = [(r*0.6, 8, 'black'), (r*0.9, 8, 'black'), (r*0.9, 4, 'red')]
		#self.hands = [(r*0.6, 8, 'black'), (r*0.9, 8, 'black'), (r*0.9, 4, 'red')]
		t = datetime.now()
		tick = -2 * pi / 60.0
		seconds = t.second + t.microsecond/1000000.0
		minutes = t.minute + seconds/60.0
		hours = (t.hour % 12) + minutes/60.0
		self.hands[0] = 5 * tick * hours
		self.hands[1] = tick * minutes
		self.hands[2] = tick * seconds
		#print(type(self.hands))
		for l, w, color in self.hands:
			#shape = ShapeNode(ui.Path.rounded_rect(0, 0, w, l, w/2), color)
			shape = ui.Path.rounded_rect(0, 0, w, l, w/2)
			#shape.anchor_point = (0.5, 0)
			shape.stroke()
			#self.hands.append(shape)
			#self.face.add_child(shape)
			
			
			
class Clock (Scene):
	def setup(self):
		print(self.size)
		r = min(self.size)/2 * 0.9
		circle = ui.Path.oval(0, 0, r*2, r*2)
		circle.line_width = 6
		shadow = ('black', 0, 0, 15)
		self.face = ShapeNode(circle, 'white', 'silver', shadow=shadow)
		self.add_child(self.face)
		for i in range(12):
			label = LabelNode(str(i+1), font=('HelveticaNeue-UltraLight', 0.2*r))
			label.color = 'black'
			a = 2 * pi * (i+1)/12.0
			label.position = sin(a)*(r*0.85), cos(a)*(r*0.85)
			self.face.add_child(label)
		self.hands = []
		hand_attrs = [(r*0.6, 8, 'black'), (r*0.9, 8, 'black'), (r*0.9, 4, 'red')]
		for l, w, color in hand_attrs:
			shape = ShapeNode(ui.Path.rounded_rect(0, 0, w, l, w/2), color)
			shape.anchor_point = (0.5, 0)
			self.hands.append(shape)
			self.face.add_child(shape)
		self.face.add_child(ShapeNode(ui.Path.oval(0, 0, 15, 15), 'black'))
		self.did_change_size()
		
	def did_change_size(self):
		self.face.position = self.size/2
		
	def update(self):
		t = datetime.now()
		tick = -2 * pi / 60.0
		seconds = t.second + t.microsecond/1000000.0
		minutes = t.minute + seconds/60.0
		hours = (t.hour % 12) + minutes/60.0
		self.hands[0].rotation = 5 * tick * hours
		self.hands[1].rotation = tick * minutes
		self.hands[2].rotation = tick * seconds
		
if __name__ == '__main__':
	is_scene_clock = False
	if is_scene_clock:
		run(Clock())
	else:
		v = Clock2()
		v.present('sheet')

