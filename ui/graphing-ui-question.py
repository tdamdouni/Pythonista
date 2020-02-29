from __future__ import print_function
# https://forum.omz-software.com/topic/3203/graphing-ui-question/6

import ui

_list = ['Rect', 'Oval', 'Rounded_Rect', 'Polygon']
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		
		self.tv = None
		#self.tv_r = ui.Rect(*self.bounds)
		#self.tv_r.width *= .25
		self.make_view()
		self.tv.selected_row = 0
		
	def make_view(self):
		tv = ui.TableView()
		tv.data_source = ui.ListDataSource(_list)
		self.add_subview(tv)
		self.tv = tv
		tv.delegate = self
		
	def layout(self):
		r = ui.Rect(*self.frame)
		r.width *= .33
		self.tv.frame = r
		
	def draw(self):
		# the shape drawing area
		r = ui.Rect(*self.frame)
		ui.set_color('teal')
		r.width -= self.tv.width
		r.x = self.tv.bounds.max_x
		r.y = self.tv.bounds.y
		s = ui.Path.rect(*r)
		s.fill()
		ui.set_color('blue')
		s.stroke()
		
		# square the rectangle to draw the shape into
		r1 = ui.Rect(r.x, r.y, r.width, r.width).inset(5, 5)
		r1.center(r.center())
		ui.set_color('white')
		
		# draw the shape based on the list selection
		txt_type = self.get_selected_row_data()
		if txt_type is 'Rect':
			s1 = ui.Path.rect(*r1)
		elif txt_type is 'Oval':
			s1 = ui.Path.oval(*r1)
		elif txt_type is 'Rounded_Rect':
			s1 = ui.Path.rounded_rect(r1[0], r1[1], r1[2], r1[3], 3)
			#s1 = ui.Path.rounded_rect(*r1, 3)
		elif txt_type is 'Polygon':
			s1 = ui.Path.rect(*r1)
			print('ok, thats for you to implement...')
			
		s1.fill()
		
	def get_selected_row_data(self):
		return self.tv.data_source.items[self.tv.selected_row[1]]
		
	def tableview_did_select(self, tableview, section, row):
		self.set_needs_display()
		
if __name__ == '__main__':
	w = 600
	h = 800
	f = (0, 0, w, h)
	mc = MyClass(frame = f, bg_color = 'white', name = 'Shapes Demo')
	mc.present('sheet')
	
# --------------------

