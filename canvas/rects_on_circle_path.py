# coding: utf-8

# https://forum.omz-software.com/topic/3449/share-a-list-of-rects-distributed-around-360-degrees/9

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
	#def __init__(self, *args, **kwargs):
		#super().__init__(*args, **kwargs)
		
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

