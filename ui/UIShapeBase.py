# https://gist.github.com/Phuket2/3ac381ddd613c0a4b72497e6e57413e7

# https://forum.omz-software.com/topic/3208/ui-path-append_path-other_path-diff-line_width-values/7

# Forum @Phuket2

import ui, editor

class UIShapeBase(object):
	def __init__(self, frame, *args, **kwargs):
		self.frame = ui.Rect(*frame)
		self.margin = (0, 0)
		self.origin = (0, 0)
		self.shape = None
		self.alpha = 1
		self.f_clr = 'white'    # fill color
		self.s_clr = 'black'    # stroke color
		self.line_width = .4
		self.shadow = None
		
		self.draw_stroke = True
		self.draw_fill = True
		self.draw_shadow = False
		self.draw_rotate = False
		self.set_kwargs(**kwargs)
		
	@property
	def bounds(self):
		return ui.Rect(*self.frame).inset(*self.margin).translate(self.origin[0], self.origin[1])
		
	@property
	def get_shape(self):
		return ui.Rect(*self.frame).inset(*self.margin).translate(self.origin[0], self.origin[1])
		
	def fill(self):
		with ui.GState():
			ui.set_color(self.f_clr)
			self.shape.line_width = self.line_width
			self.shape.fill()
			
	def stroke(self):
		with ui.GState():
			ui.set_color(self.s_clr)
			ui.set_shadow('darkgray', .5, .5, 8)
			self.shape.line_width = self.line_width
			self.shape.stroke()
			
	def fill_bounds(self):
		with ui.GState():
			s = self.get_bounds_shape()
			s.fill()
			
	def stroke_bounds(self):
		with ui.GState():
			s = self.get_bounds_shape()
			s.line_width = self.line_width
			s.stroke()
			
	def get_bounds_shape(self):
		return ui.Path.rect(*self.bounds)
		
	def render(self):
		if self.draw_fill:
			self.fill()
		if self.draw_stroke:
			self.stroke()
			
	def raw_render(self):
		# do nothing to the shape. render as coded
		s = self.make_shape()
		
		if self.draw_fill:
			s.fill()
			
		if self.draw_stroke:
			s.stroke()
			
			
	def add_shape(self):
		pass
		
	def set_kwargs(self, **kwargs):
		for k, v in kwargs.items():
			if hasattr(self, k):
				setattr(self, k, v)
				
class UIShapeOval(UIShapeBase):
	def __init__(self, frame, *args, **kwargs):
		super().__init__(frame, *args, **kwargs)
		self.shape = self.make_shape()
		
	def make_shape(self):
		return ui.Path.oval(*self.bounds)
		
class UIShapeGrid(UIShapeBase):
	def __init__(self, frame, *args, **kwargs):
		super().__init__(frame, *args, **kwargs)
		self.shape = self.make_shape()
		self.draw_stroke = True
		self.draw_fill = False
		self.f_clr = 'teal'
		
	def make_shape(self):
		# draw a grid
		w=50
		h=w
		r = self.bounds
		s = ui.Path.rect(*r)
		iter = int(r.width / w)
		for i in range(1 , iter):
			s.move_to(r.x + (i * w), r.y)
			s.line_to(r.x + (i * w), r.max_y)
			
		iter = int(r.height / h)
		for i in range(1 , iter):
			s.move_to(r.y, r.x + (i * w))
			s.line_to(r.max_y, r.x + (i * w))
			
		s.close()
		return s
		
class UIShapeClockFace(UIShapeBase):
	def __init__(self, frame, *args, **kwargs):
		super().__init__(frame, *args, **kwargs)
		self.draw_fill = False
		self.shape = self.make_shape()
		self.s_clr = 'navy'
		
	def make_shape(self):
		ln_width = 30
		with ui.GState():
			r = ui.Rect(*self.bounds).inset(ln_width / 2, ln_width /2)
			s = ui.Path.oval(*r)
			s.line_width = ln_width
			
		with ui.GState():
			s2 = ui.Path.rect(*s.bounds)
			s2.line_width = .5
			s.append_path(s2)
			s.close()
			
		s.stroke()
		return s
		
		
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		f = (0, 0, 300, 300)
		self.grid = UIShapeGrid(f, origin = (100, 100), s_colr = 'orange')
		self.oval = UIShapeOval(f, origin = (100, 100), f_clr = 'lime', s_colr = 'white', margin = (2, 2))
		self.clockface = UIShapeClockFace(f, origin = (100, 100), s_clr = 'white', margin = (30, 30), f_clr = 'deeppink')
		
	def draw(self):
		self.grid.render()
		self.oval.render()
		self.oval.render()
		self.clockface.raw_render()
		
		
if __name__ == '__main__':
	w = 600
	h = 800
	f = (0, 0, w, h)
	mc = MyClass(frame = f, bg_color = 'white')
	mc.present('sheet', animated = False)
	
	#editor.present_themed(mc, theme_name='Cool Glow', style = 'sheet', animated = False)

