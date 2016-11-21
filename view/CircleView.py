# coding: utf-8

# https://gist.github.com/Phuket2/7e4ca4cca3ed389a0e766e829959f76a

# https://forum.omz-software.com/topic/3042/ui-draw_string-vertical-alignment

import ui
import functools
import time
import string

# decorator memoize copied from ....
# https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
# note that this decorator ignores **kwargs

from objc_util import *


def get_font_list():
	# copied from - omz posting
	# https://forum.omz-software.com/topic/2024/sounds-fonts/9
	UIFont = ObjCClass('UIFont')
	all_fonts = []
	families = UIFont.familyNames()
	for family in families:
		names = UIFont.fontNamesForFamilyName_(str(family))
		all_fonts += names
	return all_fonts
	
	
def memoize(obj):
	cache = obj.cache = {}
	
	@functools.wraps(obj)
	def memoizer(*args, **kwargs):
		if args not in cache:
			cache[args] = obj(*args, **kwargs)
		return cache[args]
	return memoizer
	
	
class CircleText(ui.View):
	'''
	CircleText Class- Draw text in a circle
	'''
	
	def __init__(self, *args, **kwargs):
		self.text = '0'
		self.inset_rect = ui.Rect()
		self.circle_color = 'teal'
		self.circle_alpha = 1
		self.circle_inset = ui.Rect()
		self.font_name = 'Arial Rounded MT Bold'
		self.text_color = 'white'
		
		self.process_kwargs(**kwargs)
		
	def process_kwargs(self, **kwargs):
		for k, v in kwargs.iteritems():
			if hasattr(self, k):
				setattr(self, k, v)
				
	def update_attrs(self, **kwargs):
		'''
		CircleText.update_attrs
		params - **kwargs
		A way to update the attrs eg.font_name. calls set_needs_display
		after setting the attrs.
		'''
		self.process_kwargs(**kwargs)
		self.set_needs_display()
		
	def draw(self):
		r = ui.Rect(*self.bounds).inset(*self.circle_inset)
		
		
		oval = ui.Path.oval(r.x, r.y, r.width, r.height)
		c = ui.parse_color(self.circle_color)
		nc = (c[0], c[1], c[2], self.circle_alpha)      # color with alpha
		pattern = '9' * len(self.text)
		
		text_rect = ui.Rect(0, 0, r.width * .8, r.height * .6)
		text_rect.center(r.center())
		fs = self.get_max_fontsize(text_rect, pattern,
		self.font_name, self.inset_rect)
		
		with ui.GState():
			ui.set_color(nc)
			oval.fill()
			ui.draw_string(self.text, rect=text_rect,
			font=(self.font_name, fs), color = self.text_color,
			alignment=ui.ALIGN_CENTER,
			line_break_mode=ui.LB_TRUNCATE_TAIL)
			j = ui.Path.rect(*text_rect)
			ui.set_color((0,0,0, .5))
			j.fill()
			
			
	@memoize
	def get_max_fontsize(self, r, text, font_name, inset_rect):
		r1 = ui.Rect(*r).inset(*inset_rect)
		
		for i in xrange(5, 1000):
			w, h = ui.measure_string(text, max_width=0,
			font=(font_name, i), alignment=ui.ALIGN_CENTER,
			line_break_mode=ui.LB_TRUNCATE_TAIL)
			
			if w > r1.width or h > r1.height:
				return (i - 1)
				
if __name__ == '__main__':
	f = (0, 0, 400, 400)
	ct = CircleText(frame = f, bg_color = 'white',text_color = 'white', font_name = 'Apple SD Gothic Neo')
	ct.present('sheet')
	
	
	for i in xrange(120):
		ct.update_attrs(text = str(i))
		time.sleep(.02)

