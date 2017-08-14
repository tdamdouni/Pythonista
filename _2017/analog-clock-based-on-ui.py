# https://forum.omz-software.com/topic/4168/analog-clock-example-to-ui-example-help/2

import ui


from math import pi, sin, cos
from datetime import datetime


LabelNode = ui.Label
SpriteNode = ui.ImageView
class ShapeNode(ui.View):
	def __init__(self, path=None, fill_color='white', stroke_color='clear', shadow=None, *args, **kwargs):
		self.path = path
		self.fill_color = fill_color
		self.stroke_color = stroke_color
		super().__init__(*args, **kwargs)
		
	def draw(self):
		ui.set_color(self.fill_color)
		self.path.fill()
		ui.set_color(self.stroke_color)
		self.path.stroke()
		
class AnalogClock(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		center_x, center_y = self.center
		self.w1 = min(self.height, self.width)
		center_x, center_y = (self.w1/2, self.w1/2)
		r = (self.w1/2) * 0.9
		#print(r)
		circle = ui.Path.oval(0, 0, r*2, r*2)
		circle.line_width = 6
		shadow = ('black', 0, 0, 15)
		frame = (center_x -r, center_y - r, 2*r, 2*r)
		self.face = ShapeNode(circle, 'white', 'silver', shadow=shadow, frame=frame )
		self.add_subview(self.face)
		for i in range(12):
			a = 2 * pi * (i+1)/12.0 -pi/2
			label = LabelNode(text='{:2d}'.format(i+1), font=('HelveticaNeue-UltraLight', 0.2*r),
			text_color='black',
			frame=(cos(a)*(r*0.85)+center_x-.1*r, sin(a)*(r*0.85)+center_y-r*.85, 2*r*.85, 2*r*.85))
			self.add_subview(label)
		self.hands = []
		self.update_interval = .1
		hand_attrs = [(r*0.6, 8, 'black'), (r*0.9, 8, 'black'), (r*0.9, 4, 'red')]
		for l, w, color in hand_attrs:
			shape = ShapeNode(ui.Path.rounded_rect(l-w/2, 0, w, l, w/2), color,
			frame=(center_x-l, center_y-l, 2*l, 2*l))
			#shape.anchor_point = (0.5, 0)
			self.hands.append(shape)
			self.add_subview(shape)
		self.add_subview(ShapeNode(ui.Path.oval(0, 0, 15, 15), 'black',
		frame=(center_x-7.5, center_y-7.5, 15, 15)))
		
	def update(self):
		t = datetime.now()
		tick = 2 * pi / 60.0
		seconds = t.second + t.microsecond/1000000.0
		minutes = t.minute + seconds/60.0
		hours = (t.hour % 12) + minutes/60.0
		self.hands[0].transform = ui.Transform.rotation(5 * tick * hours)
		self.hands[1].transform = ui.Transform.rotation(tick * minutes)
		self.hands[2].transform = ui.Transform.rotation(tick * seconds)
		
		
v = ui.View(frame=(0,0,600,600))
v1 = AnalogClock(frame=(0,0,200,200))
v2 = AnalogClock(frame=(0,300,200,200))
v3 = AnalogClock(frame=(300,0,200,200))
v4 = AnalogClock(frame=(300,300,200,200))
v.add_subview(v1)
v.add_subview(v2)
v.add_subview(v3)
v.add_subview(v4)
v.present('sheet')

