# https://forum.omz-software.com/topic/3113/share-a-skeleton-for-making-and-testing-variable-height-cells-for-a-scrollview/25

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
	
# --------------------

#!python3
import ui
from random import randint

def make_cell():
	cell = ui.TableViewCell()
	
	h = randint(44, 90)
	cell.height = h
	cell.text_label.text = 'cell height - ' + str(h)
	return cell
	
class MyTableViewDataSource (object):
	def __init__(self):
		self.row_heights = None
		
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 1
		
	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		num_rows = 500
		if not self.row_heights:
			self.row_heights = [44] * num_rows
		return num_rows
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = make_cell()
		self.row_heights[row] = cell.height
		return cell
		print('in get cell', str(row))
		cell = ui.TableViewCell()
		cell.text_label.text = 'Foo Bar'
		return cell
		
	def tableview_title_for_header(self, tableview, section):
		# Return a title for the given section.
		# If this is not implemented, no section headers will be shown.
		return 'Some Section'
		
	def tableview_can_delete(self, tableview, section, row):
		# Return True if the user should be able to delete the given row.
		return True
		
	def tableview_can_move(self, tableview, section, row):
		# Return True if a reordering control should be shown for the given row (in editing mode).
		return True
		
	def tableview_delete(self, tableview, section, row):
		# Called when the user confirms deletion of the given row.
		pass
		
	def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
		# Called when the user moves a row with the reordering control (in editing mode).
		pass
		
	def tableview_height_for_section_row(self, tv,section,row):
		print('height -', str(self.row_heights[row]))
		return self.row_heights[row]
		#return 10+(row/5)**2 if row<50 else 10+((100-row)/5)**2
		
import tableview_rowheight, ui, objc_util
# create a tableview and delegate and datasource, per usual
#tableview_rowheight.setup_tableview_swizzle(False)
t=ui.TableView(frame=(0,0,200,576))
d= MyTableViewDataSource() #ui.ListDataSource([str(x) for x in range(100)])
t.data_source=t.delegate=d

# here i will just create height that grows then shrinks again
#def tableview_height_for_section_row(tv,section,row):
	#return 10+(row/5)**2 if row<50 else 10+((100-row)/5)**2
	
#d.tableview_height_for_section_row=tableview_height_for_section_row

# this is optional, but speeds up initial display and scrolling
# set to nominal or average height
t_o=objc_util.ObjCInstance(t)
t_o.estimatedRowHeight=44

t.present('sheet')
# --------------------
UITableViewAutomaticDimension# --------------------
UIViewAutoresizingNone                 = 0
UIViewAutoresizingFlexibleLeftMargin   = 1 << 0
UIViewAutoresizingFlexibleWidth        = 1 << 1
UIViewAutoresizingFlexibleRightMargin  = 1 << 2
UIViewAutoresizingFlexibleTopMargin    = 1 << 3
UIViewAutoresizingFlexibleHeight       = 1 << 4
UIViewAutoresizingFlexibleBottomMargin = 1 << 5

ObjCInstance(v).autoresizeMask=UIViewAutoResizingFlexibleWidth+UIViewAutoResizingWidth
# --------------------
import ui
from objc_util import *


class TableData(object):
	def __init__(self):
		self.data = [{'value': str(i), 'height': i+40} for i in range(10)]
		
	def tableview_number_of_rows(self, tableview, section):
		return len(self.data)
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		label = ui.Label()
		label.text = self.data[row]['value']
		label.number_of_lines = 0
		label_objc = ObjCInstance(label)
		UIViewAutoresizingFlexibleTopMargin = 1 << 5
		UIViewAutoresizingFlexibleBottomMargin = 1 << 5
		UIViewAutoresizingFlexibleHeight = 1 << 5
		UIViewAutoresizingFlexibleLeftMargin = 1 << 5
		label_objc.autoresizeMask = UIViewAutoresizingFlexibleTopMargin + UIViewAutoresizingFlexibleBottomMargin + UIViewAutoresizingFlexibleHeight + UIViewAutoresizingFlexibleLeftMargin
		label.height = self.data[row]['height']
		cell.content_view.add_subview(label)
		return cell
		
		
tv = ui.TableView()
tv.data_source = TableData()
tv_objc = ObjCInstance(tv)
tv_objc.rowHeight = -1.0 #UITableViewAutomaticDimension
tv_objc.estimatedRowHeight = 40.0
tv.present()

# --------------------

import ui
from objc_util import *


class TableData(object):
	def __init__(self):
		self.data = [{'value': str(i), 'height': i+40} for i in range(10)]
		
	def tableview_number_of_rows(self, tableview, section):
		return len(self.data)
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		label = ui.Label()
		label.text = self.data[row]['value']
		label.number_of_lines = 0
		label_objc = ObjCInstance(label)
		UIViewAutoresizingNone = 0
		UIViewAutoresizingFlexibleLeftMargin = 1 << 0
		UIViewAutoresizingFlexibleWidth = 1 << 1
		UIViewAutoresizingFlexibleRightMargin = 1 << 2
		UIViewAutoresizingFlexibleTopMargin = 1 << 3
		UIViewAutoresizingFlexibleHeight = 1 << 4
		UIViewAutoresizingFlexibleBottomMargin = 1 << 5
		
		label_objc.autoresizeMask = UIViewAutoresizingFlexibleWidth + UIViewAutoresizingFlexibleTopMargin + UIViewAutoresizingFlexibleBottomMargin + UIViewAutoresizingFlexibleHeight
		label.height = self.data[row]['height']
		cell.content_view.add_subview(label)
		return cell
		
		
tv = ui.TableView()
tv.data_source = TableData()
tv_objc = ObjCInstance(tv)
tv_objc.rowHeight = -1.0 #UITableViewAutomaticDimension
tv_objc.estimatedRowHeight = 40.0
tv.present()

# --------------------

import ui, faker, random
from objc_util import *

f=faker.Faker()
items=[f.text(random.randint(10,200)) for i in range(20)]

class MyTableViewDataSource (object):

	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return 20
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		cell.text_label.text = items[row]
		cell.text_label.number_of_lines=0
		return cell
		
		
v=ui.TableView()
v.frame=(0,0,320,576)
v.row_height=-1
v.data_source=MyTableViewDataSource()
ObjCInstance(v).estimatedRowHeight=44
v.present('sheet')
# --------------------

