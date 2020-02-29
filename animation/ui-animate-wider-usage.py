# coding: utf-8

# https://forum.omz-software.com/topic/2928/ui-animate-wider-usage/4

from __future__ import print_function
import ui

class CircleProgress(ui.View):
	def __init__(self, *args , **kwargs):
		self.min = 0.
		self.max = 1.0
		self.v = 0.
		self.increments = .01
		self.margin = (0,0,0,0)
		self.drawing_on = True
		self.alpha = 1
		self.fill_color = 'red'
		self.stroke_color = 'black'
		
		self.font =('Arial Rounded MT Bold', 18)
		self.label_on = True
		
		self.set_attrs(**kwargs)
		
		btn = ui.Button(name = 'inc')
		btn.action = self.animate
		btn.width = self.width
		btn.height = self.height
		btn.flex = 'wh'
		self.add_subview(btn)
		btn.bring_to_front()
		
	def inc(self, sender = None):
		self.value += self.increments
		if self.value > self.max: self.value = self.min
		self.set_needs_display()
		
	def dec(self):
		self.value -= self.increments
		if self.value < self.min: self.value = self.max
		self.set_needs_display()
		
	def value(self, v):
		if v < self.min or v > self.max:
			return
		self.value = v
		
		self.set_needs_display()
		
	def draw(self):
		if not self.drawing_on : return
		
		cr = ui.Rect(*self.bounds).inset(*self.margin)
		
		p = max(0.0, min(1.0, self.value))
		r = cr.width / 2
		path = ui.Path.oval(*cr)
		path.line_width = .5
		ui.set_color(self.stroke_color)
		path.stroke()
		center = ui.Point(r, r)
		path.move_to(center.x, center.y)
		start = radians(-90)
		end = start + p * radians(360)
		path.add_arc(r, r, r, start, end)
		path.close()
		ui.set_color(self.fill_color)
		path.eo_fill_rule = True
		path.fill()
		
		self.draw_label()
		
	def draw_label(self):
		if not self.drawing_on : return
		if not self.label_on: return
		
		cr = ui.Rect(*self.bounds)
		ui.set_color('purple')
		s = str('{:.0%}'.format(self.v))
		
		dim = ui.measure_string(s, max_width=cr.width, font=self.font, alignment=ui.ALIGN_CENTER, line_break_mode=ui.LB_TRUNCATE_TAIL)
		
		lb_rect = ui.Rect(0,0, dim[0], dim[1])
		lb_rect.center(cr.center())
		
		ui.draw_string(s, lb_rect , font=self.font, color='black', alignment=ui.ALIGN_CENTER, line_break_mode=ui.LB_TRUNCATE_TAIL)
		
	def set_attrs(self, **kwargs):
		for k,v in kwargs.iteritems():
			if hasattr(self, k):
				setattr(self, k, v)
				
	def animate(self, sender = None):
		print('in animate...')
		def animation():
			self.alpha = 0 # fade out
			self.value = self.alpha
			self.set_needs_display()
		ui.animate(animation, duration=2)

