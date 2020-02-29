# coding: utf-8

# https://gist.github.com/Phuket2/24ec6cd46ce76e74e4cd

# https://forum.omz-software.com/topic/2919/making-arcs-and-filling-them-with-in-ui-path/11

from __future__ import print_function
import ui
import time
from math import pi, sin, cos, radians

# a dict for kwargs shortcuts 
_indicator_attr_short_cuts = \
	{
		'cw' 		: 'cell_width',
		'ch'		: 'cell_height',
		'inc' 	: 'increments' ,
		'fc'		: 'fill_color', 
	}

class Indicator(ui.View):
	def __init__(self, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		# the idea is that this class handles all the aspects of the
		# indicator expect for the drawing. Just trying this idea,
		# rathing than subclassing. who knows, i dont. Just trying...
		# the idea is to create this class first, then create a ....

		self.min = 0.0
		self.max = 1.0
		self.increments = .1
		self.value= 0
		self.min_max_wrap = True
		self.cell_width = 50
		self.cell_height = 50
		self.fill_color = 'orange'
		self.stroke = 'red'
		
		
		
		self.draw_obj = indicator_progress1(self)
		
		# set the attrs to the kwargs
		for k,v in kwargs.iteritems():
			
			# look at the shortcuts for attr names without reducing the
			# readability of the code
			if _indicator_attr_short_cuts.get(k , None):
				k = _indicator_attr_short_cuts.get(k)
			
			if hasattr(self, k):
				setattr(self, k, v)
		
		self.width = self.cell_width 
		self.height = self.cell_height
		self.cv_rect = None
		
	def get_cell(self):
		return ui.Rect(0,0, self.cell_width , self.cell_height)
		
	def increment(self, inc = None, redraw = True):
		if not inc:
			self.value += self.increments
		else:
			self.value += inc

		if self.min_max_wrap:
			if self.value > self.max:
				self.value = self.min

		if redraw: self.set_needs_display()

	def decrement(self, dec = None, redraw = True):
		if not dec:
			self.value -= self.increments
		else:
			self.value -= dec

		if self.min_max_wrap:
			if self.value < self.min:
				self.value = self.max

		if redraw: self.set_needs_display()
	
	@property
	def cv(self):
		# the content view
		return ui.Rect(*self.bounds)
		
	@property
	def owner(self):
		return self
		
	def draw(self):
		self.draw_obj.owner_draw()
	
class indicator_progress1(object):
	def __init__(self, owner):
		self.owner = owner
		owner.min = 0.
		owner.max = 1.0
		owner.increments = .01

		
	def layout(self):
		self.frame = owner.cv 
	
	def owner_draw(self):
		owner = self.owner
	
		cell_rect = owner.cv
		
		p = max(0.0, min(1.0, owner.value))
		r = cell_rect.width / 2
		ui.set_color(owner.fill_color)
		
		path = ui.Path.oval(*cell_rect.inset(1, 1))	
		path.line_width = .5
		center = ui.Point(r, r)
		path.move_to(center.x, center.y)
		start = radians(-90)
		end = start + p * radians(360)
		path.add_arc(r, r, r, start, end)
		path.close()
		ui.set_color(owner.fill_color)
		path.eo_fill_rule = True
		path.fill()
		
		self.draw_label()
		
	def draw_label(self):
		owner = self.owner
		ui.set_color('purple')
		s = str('{:.0%}'.format(owner.value))
		lb_rect = ui.Rect(*owner.cv)
		lb_rect.center(owner.center)
		ui.draw_string(s, lb_rect , font=('Arial Rounded MT Bold', 22), color='black', alignment=ui.ALIGN_CENTER, line_break_mode=ui.LB_TRUNCATE_TAIL)
		
	def hit_test():
		pass
		
class SliderTestControl(ui.View):
	def __init__(self, parent, title , my_action = None, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		
		self.parent = parent
		self.slider = None
		self.label = None
		
		self.title = title
		self.width_percent = .8
		self.show_border = True
		self.font = ('Arial Rounded MT Bold', 18)
		
		self.make_view()
		
		# set the attrs to the kwargs
		for k,v in kwargs.iteritems():
			if hasattr(self, k):
				setattr(self, k, v)
		
		parent.add_subview(self)
		self.slider.action = my_action 
		
		
	def make_view(self):
		self.slider = ui.Slider(name = self.title)
		if self.show_border:
			self.slider.border_width = .5
		self.add_subview(self.slider)
		
		lb = ui.Label(name = self.title)
		lb.text = self.title
		lb.font = self.font
		lb.border_width = .5
		lb.bg_color = 'orange'
		lb.size_to_fit()
		lb.alignment = ui.ALIGN_CENTER
		self.label = lb
		self.add_subview(lb)
		
	
	def layout(self):
		self.width = self.parent.width * self.width_percent
		self.height = self.slider.height + self.label.height
		
		self.slider.width = self.width
		self.label.width = self.width
		self.label.y = self.slider.height
	
		
def make_button(name, title, action):
	# just for testing
	btn = ui.Button(name = name, title = title)
	btn.action = action
	btn.width = 100
	btn.height = 32
	btn.border_width = .5
	btn.corner_radius = 3
	btn.font = ('<System-Bold>', 14)
	btn.bg_color = 'gray'
	btn.tint_color = 'orange'
	return btn

class TestClass(ui.View):
	# just for testing
	def __init__(self, indicator , *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		
		
		self.bg_color = 'white'
		self.indicator = indicator
		self.named_slider = SliderTestControl(self, 'Min - Max Slider', my_action = self.slider_min_max)
		

		self.make_view() 
		
	def make_view(self):
		btn = make_button('Next', 'Next', self.next_page)
		self.add_subview(btn)
		btn.x = self.center[0] - btn.width / 2
		btn.y = 300

		btn = make_button('Previous', 'Previous', self.prev_page)
		self.add_subview(btn)
		btn.x = self.center[0] - btn.width / 2
		btn.y = 342
		
		
		# if there is a indicator add it to the view
		if self.indicator:
			self.add_subview(self.indicator)
			
	def next_page(self, sender):
		self.indicator.increment()
		#self.animate_indicator()

	def prev_page(self, sender):
		self.indicator.decrement()
		
	@ui.in_background
	def animate_indicator(self):
		incs = .1
		self.indicator.increments = incs
		for i in xrange(0,10):
			v = incs * float(i)
			print(v)
			self.indicator.increment(v)
			time.sleep(.1) 
			if not self.on_screen:
				break
				
	def slider_min_max(self, sender)	:
		self.indicator.value = sender.value
		self.indicator.set_needs_display()
		
		
		
		
	def layout(self):
		r = ui.Rect(*self.bounds)
		self.named_slider.center = self.center
		self.named_slider.y = self.height - self.named_slider.height - 40
		return
		slider_min_max = self.get_subview_by_name('smm')
		slider_min_max.center = self.center
		slider_min_max.y = self.height - slider_min_max.height - 40
		
	
	def get_subview_by_name(self, view_name, search = None):
		# if search, traverse the views looking for the named sub_view
		if not search:
			return self[view_name]
		
if __name__ == '__main__':
	f = (0,0, 600, 800)
	ind = Indicator(fill_color = 'red', cw = 200, ch = 200)
	
	tc = TestClass(ind , frame = f)
	tc.present('sheet')
