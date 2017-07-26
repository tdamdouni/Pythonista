# https://forum.omz-software.com/topic/3449/share-a-list-of-rects-distributed-around-360-degrees

'''
    Pythonista Forum - @Phuket2
'''
import ui, editor
from math import pi, sin, cos

def rects_on_circle_path(rect_path, obj_width,
                            margin = 2, num_objs = 12):
	'''
	rects_on_circle_path
	PARAMS:
	1. rect_path = the bounding rect of the circle
	**Note the rect is inseted half of the shape_width param + the
	margin param. the resulting rects are centered on the bounding
	circle.
	
	2. obj_width = the width of the shape/rect you are placing on the
	path.
	
	3. margin = 2 , additionally insets the rect_path by this value
	
	4. num_objects = 12.  the number of objects to distribute around
	rect_path. set to 12 as default, a clock face.  odd and even
	numbers are ok.
	
	RETURNS:
	tuple(Rect, list)
	1. Rect = the adjusted rect_path after transformations in the func.
	2. a list[] containing a ui.Rect's. the length of the list is
	equal to the num_objs param.
	
	NOTES:
	For some reason i can't do the math if my life depended on it.
	I copied the math from the AnalogClock.py pythonista example.
	
	ALSO should have a param to shift the basline of the rects, off
	the center line of the rect_path.
	
	the reason why i return a list of rects in the tuple is for
	flexibility.  in the example, just drawing. but could just as
	easily be positioning ui.Button/ui.Label object or whatever.
	
	oh, btw i know its a bit of a mess. hard when you are not sure
	of the math to get it as concise as it should be.
	
	'''
	
	rects = []
	
	r = ui.Rect(*rect_path).inset((obj_width/2) + margin, (obj_width/2) + margin)
	
	radius = r.width / 2
	for i in range(0, num_objs):
		a = 2 * pi * (i+1)/num_objs
		pos = (sin(a)*(radius*1), cos(a)*(radius*1))
		r1 = ui.Rect(pos[0] , pos[1] , obj_width, obj_width)
		r1.x += ((r.width/2) - (obj_width/2)+r.x)
		r1.y += ((r.height/2) - (obj_width/2)+r.y)
		rects.append(r1)
		
	return (r,rects)
	
	
	
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	def draw(self):
		r = ui.Rect(*self.bounds)
		r, rects = rects_on_circle_path(r, 10, margin = 20 ,
		num_objs = 36 )
		s = ui.Path.oval(*r)
		ui.set_color('lime')
		s.stroke()
		
		ui.set_color('orange')
		for r in rects:
			s = ui.Path.oval(*r)
			s.fill()
			
		r = ui.Rect(*self.bounds)
		r, rects = rects_on_circle_path(r, 15, margin = 40 ,
		num_objs = 12 )
		s = ui.Path.oval(*r)
		ui.set_color('yellow')
		s.stroke()
		
		ui.set_color('purple')
		for r in rects:
			s = ui.Path.oval(*r)
			s.fill()
			
		r = ui.Rect(*self.bounds)
		r, rects = rects_on_circle_path(r, 25, margin = 80 ,
		num_objs = 6 )
		s = ui.Path.oval(*r)
		ui.set_color('orange')
		s.stroke()
		
		ui.set_color('lime')
		for r in rects:
			s = ui.Path.rect(*r)
			s.fill()
			
if __name__ == '__main__':
	_use_theme = True
	w, h = 600, 600
	f = (0, 0, w, h)
	name = 'Silly Demo'
	mc = MyClass(frame=f, bg_color='white', name = name)
	
	if not _use_theme:
		mc.present('sheet', animated=False)
	else:
		editor.present_themed(mc, theme_name='Oceanic', style='sheet', animated=False)
# --------------------
btn = make_button(i, title=self._list[i])
btn.alpha = (1+i) * (1/len(self._list)) # will go from 1/n to 1.0, where n = Len of list
self.add_subview(btn)
# --------------------
import editor
import math
import ui

# this is a pretty funky function...
def get_rotated_icon(named_icon_name, wh = 32, degree = 0):
	'''
	help from @omz
	https://forum.omz-software.com/topic/3180/understanding-ui-transform-rotation
	'''
	r = ui.Rect(0, 0, wh, wh)
	img = ui.Image.named(named_icon_name)
	with ui.ImageContext(wh, wh) as ctx:
		ui.concat_ctm(ui.Transform.translation(*r.center()))
		ui.concat_ctm(ui.Transform.rotation(math.radians(degree)))
		ui.concat_ctm(ui.Transform.translation(*r.center() * -1))
		img.draw()
		return ctx.get_image()
		
def make_button(idx, title, name = None):
	def button_action(sender):
		print('Button {} was pressed.'.format(sender.name))
		
	#btn = ui.Button(title=calendar.month_abbr[i+1])
	name = name if name else title
	btn = ui.Button(name = name, title=title )
	btn.action = button_action
	#btn.alpha = _range_12[idx]
	btn.border_width = .5
	btn.bg_color = 'white'
	btn.text_color = btn.tint_color = 'black'
	return btn
	
def css_clr_to_rgba(css_name, a):
	c = ui.parse_color(css_name)
	return (c[0], c[1], c[2], a)
	
def rects_on_circle_path(rect_path, obj_width, margin=2, num_objs=12):
	def calculate_a_rect(i):
		a = 2 * math.pi * i/num_objs - math.pi/2
		# careful: cos,sin! not sin,cos
		pos = (math.cos(a)*(radius*1), math.sin(a)*(radius*1))
		r1 = ui.Rect(*pos, obj_width, obj_width)
		r1.x += r.width / 2 - obj_width / 2 + r.x
		r1.y += r.height / 2 - obj_width / 2 + r.y
		
		return r1
		
	r = ui.Rect(*rect_path).inset(obj_width / 2 + margin,
	obj_width / 2 + margin)
	radius = r.width / 2
	return r, [calculate_a_rect(i) for i in range(num_objs)]
	
class MyClass(ui.View):
	# some ideas
	_list=['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW' ]
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.cir_rect = None
		self.obj_list = []
		self.mid_btn = None
		
		self.make_view()
		
	def make_view(self):
		for i in range(len(self._list)):
			obj = make_button(i, title=self._list[i])
			obj.image = get_rotated_icon('iob:arrow_up_a_256', wh = 256, degree = i * 45)
			self.obj_list.append(obj)
			self.add_subview(obj)
			
		btn = make_button(i, title='C')
		self.mid_btn = btn
		self.add_subview(btn)
		
		
	def layout(self):
		r, rects = rects_on_circle_path(self.bounds, obj_width=70,                              margin=20, num_objs=len(self._list))
		self.cir_rect = r
		for i, btn in enumerate(self.obj_list):
			btn.frame = rects[i]
			btn.title = ''
			btn.corner_radius = btn.width / 2
			
		btn = self.mid_btn
		btn.center = r.center()
		btn.corner_radius = btn.width / 2
		
	def draw(self):
		# just to see the path when testing...
		s = ui.Path.oval(*self.cir_rect)
		with ui.GState():
			ui.set_color(css_clr_to_rgba('lime', .4))
			s.line_width = 1
			s.stroke()
			
			
if __name__ == '__main__':
	_use_theme = True
	w=h = 600
	f = (0, 0, w, h)
	
	mc = MyClass(frame=f, bg_color='white')
	
	if not _use_theme:
		mc.present('sheet', animated=False)
	else:
		editor.present_themed(mc, theme_name='Oceanic', style='sheet', animated=False)
		
# --------------------
'''
    Pythonista Forum - @Phuket2
'''
import ui, editor
from math import pi, sin, cos

def rects_on_circle_path(rect_path, obj_width,
                            margin = 2, num_objs = 12):
	'''
	rects_on_circle_path
	PARAMS:
	1. rect_path = the bounding rect of the circle
	**Note the rect is inseted half of the shape_width param + the
	margin param. the resulting rects are centered on the bounding
	circle.
	
	2. obj_width = the width of the shape/rect you are placing on the
	path.
	
	3. margin = 2 , additionally insets the rect_path by this value
	
	4. num_objects = 12.  the number of objects to distribute around
	rect_path. set to 12 as default, a clock face.  odd and even
	numbers are ok.
	
	RETURNS:
	tuple(Rect, list)
	1. Rect = the adjusted rect_path after transformations in the func.
	2. a list[] containing a ui.Rect's. the length of the list is
	equal to the num_objs param.
	
	NOTES:
	For some reason i can't do the math if my life depended on it.
	I copied the math from the AnalogClock.py pythonista example.
	
	ALSO should have a param to shift the basline of the rects, off
	the center line of the rect_path.
	
	the reason why i return a list of rects in the tuple is for
	flexibility.  in the example, just drawing. but could just as
	easily be positioning ui.Button/ui.Label object or whatever.
	
	oh, btw i know its a bit of a mess. hard when you are not sure
	of the math to get it as concise as it should be.
	
	'''
	
	rects = []
	
	r = ui.Rect(*rect_path).inset((obj_width/2) + margin, (obj_width/2) + margin)
	
	radius = r.width / 2
	for i in range(0, num_objs):
		a = 2 * pi * (i+1)/num_objs
		pos = (sin(a)*(radius*1), cos(a)*(radius*1))
		r1 = ui.Rect(pos[0] , pos[1] , obj_width, obj_width)
		r1.x += ((r.width/2) - (obj_width/2)+r.x)
		r1.y += ((r.height/2) - (obj_width/2)+r.y)
		rects.append(r1)
		
	return (r,rects)
	
	
	
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	def draw(self):
		r = ui.Rect(*self.bounds)
		r, rects = rects_on_circle_path(r, 10, margin = 20 ,
		num_objs = 36 )
		s = ui.Path.oval(*r)
		ui.set_color('lime')
		s.stroke()
		
		ui.set_color('orange')
		for r in rects:
			s = ui.Path.oval(*r)
			s.fill()
			
		r = ui.Rect(*self.bounds)
		r, rects = rects_on_circle_path(r, 15, margin = 40 ,
		num_objs = 12 )
		s = ui.Path.oval(*r)
		ui.set_color('yellow')
		s.stroke()
		
		ui.set_color('purple')
		for r in rects:
			s = ui.Path.oval(*r)
			s.fill()
			
		r = ui.Rect(*self.bounds)
		r, rects = rects_on_circle_path(r, 25, margin = 80 ,
		num_objs = 6 )
		s = ui.Path.oval(*r)
		ui.set_color('orange')
		s.stroke()
		
		ui.set_color('lime')
		for r in rects:
			s = ui.Path.rect(*r)
			s.fill()
			
if __name__ == '__main__':
	_use_theme = True
	w, h = 600, 600
	f = (0, 0, w, h)
	name = 'Silly Demo'
	mc = MyClass(frame=f, bg_color='white', name = name)
	
	if not _use_theme:
		mc.present('sheet', animated=False)
	else:
		editor.present_themed(mc, theme_name='Oceanic', style='sheet', animated=False)
# --------------------
def rects_on_circle_path(rect_path, obj_width,
                            margin = 2, num_objs = 12):
	rects = []
	
	r = ui.Rect(*rect_path).inset((obj_width/2) + margin, (obj_width/2) + margin)
	
	radius = r.width / 2
	for i in range(0, num_objs):
		a = 2 * pi * (i+1)/num_objs
		a += radians(-210) # <---- changed this
		
		pos = (sin(a)*(radius*1), cos(a)*(radius*1))
		r1 = ui.Rect(pos[0] , pos[1] , obj_width, obj_width)
		r1.x += ((r.width/2) - (obj_width/2)+r.x)
		r1.y += ((r.height/2) - (obj_width/2)+r.y)
		rects.append(r1)
		
	return (r,rects)
# --------------------
a = -2 * pi * (i+1)/num_objs # inverse
a += radians(-150) # change delta
# --------------------
# Normally, in Algebra, we compute point coordinates with
#  x = r*cos(a)
#  y = r*sin(a)
#  where a is the angle versus the horizontal axe
#  positive reverse clockwise (sorry)
#  thus a = 0 for 3 hour
#  if you want index 0 at 12 hour, you need to turn 90Â° left, thus -90Â°
# thus the best solution is
a = 2 * pi * i/num_objs - pi/2
pos = (cos(a)*(radius*1), sin(a)*(radius*1)) # careful: cos,sin! not sin,cos
# --------------------
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
calculate_a_rect()# --------------------
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
def rects_on_circle_path(rect_path, obj_width, margin=2, num_objs=12):
	def calculate_a_rect(i):
		'''
		a = -2 * math.pi * (i + 1) / num_objs + math.radians(-150)
		pos = math.sin(a) * radius, math.cos(a) * radius
		r1 = ui.Rect(*pos, obj_width, obj_width)
		r1.x += r.width / 2 - obj_width / 2 + r.x
		r1.y += r.height / 2 - obj_width / 2 + r.y
		'''
		a = 2 * math.pi * (i+1)/num_objs
		pos = (math.sin(a)*(radius*1), math.cos(a)*(radius*1))
		r1 = ui.Rect(pos[0] , pos[1] , obj_width, obj_width)
		r1.x += ((r.width/2) - (obj_width/2)+r.x)
		r1.y += ((r.height/2) - (obj_width/2)+r.y)
		
		return r1
		
	r = ui.Rect(*rect_path).inset(obj_width / 2 + margin,
	obj_width / 2 + margin)
	radius = r.width / 2
	return r, [calculate_a_rect(i) for i in range(num_objs)]
# --------------------
a = -2 * math.pi * (i + 1) / num_objs + math.radians(-135)
pos = math.sin(a) * radius, math.cos(a) * radius
# --------------------
a = 2 * math.pi * i/num_objs - math.pi/2
pos = (math.cos(a)*(radius*1), math.sin(a)*(radius*1)) # careful: cos,sin! not sin,cos
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

def css_clr_to_rgba(css_name, a):
	c = ui.parse_color(css_name)
	return (c[0], c[1], c[2], a)
	
def rects_on_circle_path(rect_path, obj_width, margin=2, num_objs=12):
	def calculate_a_rect(i):
		a = 2 * math.pi * i/num_objs - math.pi/2
		# careful: cos,sin! not sin,cos
		pos = (math.cos(a)*(radius*1), math.sin(a)*(radius*1))
		r1 = ui.Rect(*pos, obj_width, obj_width)
		r1.x += r.width / 2 - obj_width / 2 + r.x
		r1.y += r.height / 2 - obj_width / 2 + r.y
		
		return r1
		
	r = ui.Rect(*rect_path).inset(obj_width / 2 + margin,
	obj_width / 2 + margin)
	radius = r.width / 2
	return r, [calculate_a_rect(i) for i in range(num_objs)]
	
	
def make_button(idx, title):
	def button_action(sender):
		print('Button {} was pressed.'.format(sender.title))
		
	#btn = ui.Button(title=calendar.month_abbr[i+1])
	btn = ui.Button(title=title)
	btn.action = button_action
	#btn.alpha = _range_12[idx]
	btn.border_width = .5
	btn.bg_color = 'white'
	btn.text_color = btn.tint_color = 'black'
	return btn
	
class MyClass(ui.View):
	# some ideas
	_list=['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW' ]
	#_list=['N', 'E' , 'S' , 'W']
	#_list=['1st', '2nd', '3rd', '4th', '5th']
	#_list=['0', '90', '180', '270' ]
	#_list= [str(d) for d in range(0, 12)]
	_list = [calendar.month_abbr[i] for i in range(1,12)]
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.cir_rect = None
		self.make_view()
	def make_view(self):
		for i in range(len(self._list)):
			self.add_subview(make_button(i, title=self._list[i]))
			
	def layout(self):
		r, rects = rects_on_circle_path(self.bounds, obj_width=70,                              margin=20, num_objs=len(self._list))
		self.cir_rect = r
		for i, btn in enumerate(self.subviews):
			btn.frame = rects[i]
			btn.title = self._list[i]
			btn.corner_radius = btn.width / 2
			
	def draw(self):
		s = ui.Path.oval(*self.cir_rect)
		with ui.GState():
			ui.set_color(css_clr_to_rgba('lime', .4))
			s.line_width = 1
			s.stroke()
			
if __name__ == '__main__':
	_use_theme = True
	w = h = 500
	f = (0, 0, w, h)
	mc = MyClass(frame=f, bg_color='white', name='Silly Demo')
	
	if not _use_theme:
		mc.present('sheet', animated=False)
	else:
		editor.present_themed(mc, theme_name='Solarized Dark', style='sheet',
		animated=False)
# --------------------
import circulartextlayout
import ui


layout_text = '''
************
************
bbbbbbbbbbbb
************
i*i*i*i*i*i*
************
************
'''

image_list = [ ui.Image.named(i) for i in 'Rabbit_Face Mouse_Face Cat_Face Dog_Face Octopus Cow_Face'.split()]
_range_12 = (.3, .34, .38, .42, .46, .5, .55, .6, .63, .7, .85, 1.0)

def button_action(sender):
	print('Button {} was pressed.'.format(sender.title))
	
titles = 'jan feb mar apr may jun jul aug sep oct nov dec'.split()

attributes = {'b': [{'action':button_action, 'font' :('Helvetica', 20),
                     'bg_color':'orange', 'alpha':_range_12[i],
                     'border_width':.5, 'text_color':'black', 'tint_color':'black',
                     'title':j } for i, j in enumerate(titles)],
             'i': [{'image':i,  'bg_color':'gray'} for i in image_list ]
             }

v = circulartextlayout.BuildView(layout_text, width=600, height=600, view_name='Counter',
    attributes=attributes).build_view()

for i in range(1, len(titles)+1):
	v['button'+str(i)].corner_radius = v['button'+str(i)].width*.5
for i in range(1, len(image_list)+1):
	v['imageview'+str(i)].corner_radius = v['imageview'+str(i)].width*.5
v.present('popover')

# --------------------
btn = make_button(i, title=self._list[i])
btn.alpha = (1+i) * (1/len(self._list)) # will go from 1/n to 1.0, where n = Len of list
self.add_subview(btn)
# --------------------

