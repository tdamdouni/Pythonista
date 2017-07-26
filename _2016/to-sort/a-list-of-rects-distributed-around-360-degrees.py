# coding: utf-8

# https://forum.omz-software.com/topic/3449/share-a-list-of-rects-distributed-around-360-degrees/9

'''
    Pythonista Forum - @Phuket2
'''
import ui, editor
from math import pi, sin, cos, radians, degrees
import calendar

# example, playing around, for 12 items its ok no math :)
_range_12 = [.3, .34, .38, .42, .46 , .5, .55, .6, .63, .7, .85, 1.0]

def rects_on_circle_path(rect_path, obj_width,
                            margin = 2, num_objs = 12):

	rects = []
	
	r = ui.Rect(*rect_path).inset((obj_width/2) + margin, (obj_width/2) + margin)
	
	radius = r.width / 2
	for i in range(0, num_objs):
		#a = 2 * pi * (i+1)/num_objs
		#a += radians(-210)
		# thanks @cvp, now the rects start at 0 degrees, yeah!!
		a = -2 * pi * (i+1)/num_objs # inverse
		a += radians(-150) # change delta
		
		pos = (sin(a)*(radius*1), cos(a)*(radius*1))
		r1 = ui.Rect(pos[0] , pos[1] , obj_width, obj_width)
		r1.x += ((r.width/2) - (obj_width/2)+r.x)
		r1.y += ((r.height/2) - (obj_width/2)+r.y)
		rects.append(r1)
		
	return (r,rects)
	
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.btns = []
		self.make_view()
		
	def make_view(self):
		for i in range(0,12):
			btn = ui.Button()
			btn.title = calendar.month_abbr[i+1]
			btn.bg_color = 'orange'
			btn.tint_color = 'black'
			btn.border_width = .5
			self.add_subview(btn)
			self.btns.append(btn)
			
	def layout(self):
		r = ui.Rect(*self.bounds)
		obj_width = 80
		r, rects = rects_on_circle_path(r, obj_width, margin = 20 ,
		num_objs = 12)
		ui.set_color('orange')
		for i, btn in enumerate(self.btns):
			btn.frame = rects[i]
			btn.corner_radius = btn.width / 2
			btn.text_color = 'black'
			btn.alpha = _range_12[i]
			
if __name__ == '__main__':
	_use_theme = False
	w, h = 600, 600
	f = (0, 0, w, h)
	name = 'Silly Demo'
	mc = MyClass(frame=f, bg_color='white', name = name)
	
	if not _use_theme:
		mc.present('sheet', animated=False)
	else:
		editor.present_themed(mc, theme_name='Oceanic', style='sheet', animated=False)
		
# --------------------

'''
    Pythonista Forum - @Phuket2
'''

import calendar
import editor
import math
import ui

# example, playing around, for 12 items its ok no math :)
_range_12 = (.3, .34, .38, .42, .46, .5, .55, .6, .63, .7, .85, 1.0)


def rects_on_circle_path(rect_path, obj_width, margin=2, num_objs=12):
	def calculate_a_rect(i):
		a = -2 * math.pi * (i + 1) / num_objs + math.radians(-150)
		pos = math.sin(a) * radius, math.cos(a) * radius
		r1 = ui.Rect(*pos, obj_width, obj_width)
		r1.x += r.width / 2 - obj_width / 2 + r.x
		r1.y += r.height / 2 - obj_width / 2 + r.y
		return r1
		
	r = ui.Rect(*rect_path).inset(obj_width / 2 + margin,
	obj_width / 2 + margin)
	radius = r.width / 2
	return r, [calculate_a_rect(i) for i in range(num_objs)]
	
	
def make_button(i):
	def button_action(sender):
		print('Button {} was pressed.'.format(sender.title))
		
	btn = ui.Button(title=calendar.month_abbr[i+1])
	btn.action = button_action
	btn.alpha = _range_12[i]
	btn.border_width = .5
	btn.bg_color = 'orange'
	btn.text_color = btn.tint_color = 'black'
	return btn
	
	
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for i in range(12):
			self.add_subview(make_button(i))
			
	def layout(self):
		r, rects = rects_on_circle_path(self.bounds, obj_width=80, margin=20,
		num_objs=12)
		for i, btn in enumerate(self.subviews):
			btn.frame = rects[i]
			btn.corner_radius = btn.width / 2
			
			
if __name__ == '__main__':
	_use_theme = False
	w = h = 600
	f = (0, 0, w, h)
	mc = MyClass(frame=f, bg_color='white', name='Silly Demo')
	
	if not _use_theme:
		mc.present('sheet', animated=False)
	else:
		editor.present_themed(mc, theme_name='Oceanic', style='sheet',
		animated=False)
# --------------------

