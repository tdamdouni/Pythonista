# coding: utf-8

# https://forum.omz-software.com/topic/2907/help-with-draw-method-in-custom-class

import ui

class PageIndicator(ui.View):
	def __init__(self, *args, **kwargs):
		self.num_pages = 10
		self.w = 10
		self.h = 10
		self.factor = .6
		self.selected = 2
		self.on_color = 'orange'
		self.off_color = 'black'
		self.frame = (0,0, self.w * self.num_pages, self.h)
		
	def layout(self):
		self.width = self.w * self.num_pages
		self.height = self.h
		
	def next(self):
		if self.selected == self.num_pages:
			self.selected = 1
		else:
			self.selected += 1
			
		# self.draw()
				# edit from @dgelessus ,
			self.set_needs_display()
			
			
	def draw(self):
		ui.set_color(self.off_color)
		for i in range(0,self.num_pages +1):
			oval = ui.Path.oval(self.w * i, 0,
			self.w * self.factor, self.h * self.factor)
			if (i + 1) == self.selected:
				ui.set_color(self.on_color)
				oval.fill()
				ui.set_color(self.off_color)
			else:
				oval.fill()
				
class TestClass(ui.View):
	def __init__(self, image_mask = None, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		self.pg_ind = PageIndicator()
		self.add_subview(self.pg_ind)
		
		btn = ui.Button(title = 'Next Page')
		btn.action = self.next_page
		btn.width = 100
		btn.height = 32
		btn.border_width = .5
		btn.corner_radius = 3
		btn.bg_color = 'black'
		btn.tint_color = 'orange'
		self.add_subview(btn)
		btn.center = self.center
		
	def next_page(self, sender):
		self.pg_ind.next()
		
	def layout(self):
		pg_ind = self.pg_ind
		pg_ind.y = self.bounds.height - (pg_ind.h + 10)
		pg_ind.x = (self.bounds.width / 2 ) - (pg_ind.width / 2)
		
		
if __name__ == '__main__':
	f = (0,0, 320, 480)
	tc = TestClass( frame = f, bg_color = 'white')
	tc.present('sheet')
	
#==============================

	def draw(self):
		ui.set_color(self.off_color)
		for i in range(self.num_pages):
			oval = ui.Path.oval(self.w * i, 0,
			self.w * self.factor, self.h * self.factor)
			if i == self.selected:
				ui.set_color(self.on_color)
				oval.fill()
				ui.set_color(self.off_color)
			else:
				oval.fill()
				
#==============================

	def next(self):
		self.selected = self.selected % self.num_pages
		self.set_needs_display()

