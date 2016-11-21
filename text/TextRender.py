# https://gist.github.com/Phuket2/4c7e1191db630071e75870c60265f749

# https://forum.omz-software.com/topic/3183/share-code-rendering-text-with-ui-draw_string

import ui
import copy, math, functools

'''
        @Phuket2
        Class - UIText
        For writing text in rects.
        the instance attrs are preserved if used as a context manager
        ie, 'with'
'''


class UIText(object):
	dict_list = []
	
	def __init__(self, r=ui.Rect(), *args, **kwargs):
	
		r = ui.Rect(*r)
		# considered to be defaults
		self.rect = r
		self.text = 'SAMPLE'
		self.font_name = 'Arial Rounded MT Bold'
		self.font_size = 0
		self.text_color = 'white'
		self.margin = (0, 0)
		self.origin = (0, 0)
		self.use_shadow = True
		self.shadow_params = ('white', 0, 0, 0)
		self.rotate = 0
		
		self.do_kwargs(**kwargs)
		
	def do_kwargs(self, **kwargs):
		for k, v in kwargs.items():
			if hasattr(self, k):
				setattr(self, k, v)
				
	def get_max_fontsize(self):
		# would love some ideas for to clean this up
		# i could snapshot the params, and compare on each call. yuk
		# the loop is stupid
		r = ui.Rect(*self.rect).inset(*self.margin)
		last_w = last_h = 0
		
		for i in range(5, 1000):
			w, h = ui.measure_string(self.text, max_width=0,
			font=(self.font_name, i), alignment=ui.ALIGN_CENTER,
			line_break_mode=ui.LB_TRUNCATE_TAIL)
			
			if w > r.width or h > r.height:
				return (i - 1, ui.Rect(0, 0, last_w, last_h))
				
			last_w, last_h = w, h
			
	def draw_text(self, **kwargs):
		if kwargs:
			self.do_kwargs(**kwargs)
			
		r = ui.Rect(*self.rect).inset(*self.margin).translate(*self.origin)
		
		my_center = r.center()
		font_size = self.font_size
		
		if not font_size:
			result = self.get_max_fontsize()
			r1 = ui.Rect(*result[1])
			font_size = result[0]
		else:
			w, h = ui.measure_string(self.text, max_width=0,
			font=(self.font_name, font_size), alignment=ui.ALIGN_CENTER,
			line_break_mode=ui.LB_TRUNCATE_TAIL)
			r1 = ui.Rect(0, 0, w, h)
			
		r1.center(my_center)
		with ui.GState():
			if self.rotate:
				'''
				help from @omz
				https://forum.omz-software.com/topic/3180/understanding-ui-transform-rotation
				'''
				ui.concat_ctm(ui.Transform.translation(*r1.center()))
				ui.concat_ctm(ui.Transform.rotation(math.radians(self.rotate)))
				ui.concat_ctm(ui.Transform.translation(*r1.center() * -1))
				
			if self.use_shadow:
				ui.set_shadow(*self.shadow_params)
				
			ui.draw_string(self.text, rect=r1,
			font=(self.font_name, font_size), color=self.text_color,
			alignment=ui.ALIGN_CENTER,
			line_break_mode=ui.LB_TRUNCATE_TAIL)
			
	def __enter__(self):
		__class__.dict_list.append(copy.copy(self.__dict__))
		return self
		
	def __exit__(self, type, value, traceback):
		self.__dict__.update(__class__.dict_list.pop())
		
	def __str__(self):
		return '\n'.join('{} = {}'.format(k, v) for k, v in self.__dict__.items())
		
		
class MyClass(ui.View):
	'''
	test class, for trying UIText Class
	'''
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.r = (100, 100, 400, 400)
		self.text_class = UIText(r=self.r, text='IJ')
		
	def draw(self):
		r = self.r #(100, 100, 400, 400)
		with ui.GState():
			ui.set_color('teal')
			s = ui.Path.oval(*r)
			s.fill()
			
		self.text_class.draw_text()
		
		
if __name__ == '__main__':
	w = 600
	h = 800
	f = (0, 0, w, h)
	mc = MyClass(frame=f, bg_color='white')
	mc.present('sheet')
	
	import time
	
	with mc.text_class as txt:
		txt.shadow_params = ('white', -6, 6, 12)
		txt.text_color = 'orange'
		for i in range(0, 360):
			txt.rotate = i * -1
			txt.text = 'IJ'
			mc.set_needs_display()
			time.sleep(.01)
		txt.text_color = 'blue'
		for i in range(0, 360):
			txt.rotate = i
			txt.text = 'IJ'
			mc.set_needs_display()
			time.sleep(.01)
			
	with mc.text_class as txt:
		txt.shadow_params = ('white', -6, 6, 12)
		txt.text_color = 'orange'
		txt.font_size = 380
		for i in range(0, 360):
			txt.rotate = i
			txt.text = 'IJ'
			mc.set_needs_display()
			time.sleep(.001)
			
			
	print(mc.text_class)

