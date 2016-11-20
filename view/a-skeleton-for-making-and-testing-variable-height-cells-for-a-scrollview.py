# coding: utf-8

# https://forum.omz-software.com/topic/3113/share-a-skeleton-for-making-and-testing-variable-height-cells-for-a-scrollview

# Phuket - Pythonista Forum
# cell building test bed, python 3.xxx

import ui

from random import randint, choice


class SimpleCell(ui.View):
	def __init__(self, *args, **kwargs):
		self.set_attrs(**kwargs)
		
	def set_attrs(self, **kwargs):
		for k, v in kwargs.items():
			if hasattr(self, k):
				setattr(self, k, v)
				
	def add_label(self, text):
		lb = ui.Label()
		lb.text = text
		lb.font = ('Arial Rounded MT Bold', 32)
		lb.size_to_fit()
		lb.center = self.center
		self.add_subview(lb)
		
		
class ACell(SimpleCell):
	def __init__(self, *args, **kwargs):
		SimpleCell.__init__(self, *args, **kwargs)
		self.add_label('ACell')
		
		
class ACellGreen(SimpleCell):
	def __init__(self, *args, **kwargs):
		SimpleCell.__init__(self, *args, **kwargs)
		self.bg_color = 'green'
		self.add_label('Green')
		
		
class ACellRandom(SimpleCell):
	def __init__(self, *args, **kwargs):
		SimpleCell.__init__(self, *args, **kwargs)
		self.bg_color = (randint(0, 255) / 100.,
		randint(0, 255) / 100.,
		randint(0, 255) / 100.)
		self.add_label('Random')
		
		
class ACellRed(SimpleCell):
	def __init__(self, *args, **kwargs):
		SimpleCell.__init__(self, *args, **kwargs)
		self.add_label('Red')
		self.bg_color = 'red'
		
		
class ACellPurple(SimpleCell):
	def __init__(self, *args, **kwargs):
		SimpleCell.__init__(self, *args, **kwargs)
		self.add_label('Purple')
		self.bg_color = 'purple'
		
		
class DisplayCells(ui.View):
	tm = 20             # top margin
	vgap = 10           # vertical gap between cells
	
	def __init__(self, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		self.sv = None
		self.cells = []
		self.height_cache = self.tm
		
		self.make_view()
		
	def make_view(self):
		sv = ui.ScrollView(name='sv')
		sv.frame = self.bounds
		sv.flex = 'wh'
		self.add_subview(sv)
		self.sv = sv
		
	def add_cell(self, cell):
		self.cells.append(cell)
		cell.y = self.height_cache
		self.height_cache += (cell.height + self.vgap)
		self.sv.content_size = (0, self.height_cache)
		self.sv.add_subview(cell)
		
if __name__ == '__main__':
	# a list of cell classes selected randomly for testing
	_cells = [ACell, ACellGreen, ACellRandom, ACellRed, ACellPurple]
	w = 600
	h = 800
	
	f = (0, 0, w, h)
	
	dc = DisplayCells(frame=f, bg_color='white')
	
	for r in range(300):
		cell = choice(_cells)(width=f[2],
		height=randint(40, 200),  bg_color='pink')
		dc.add_cell(cell)
		
	dc.present('sheet')

