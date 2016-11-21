# coding: utf-8

# https://forum.omz-software.com/topic/2740/colors-for-listdatasource-items/6

import ui

t = ui.TableView()
t.background_color = 'black'
t.tint_color = 'white'
l = ui.ListDataSource(['One', 'Two'])
l.text_color = 'cyan'
l.highlight_color = 'blue'
l.background_color = 'red'
l.tint_color = 'green'
t.data_source = l
t.present()
#==============================

from ui import *

#==============================

self.background_color = None

#==============================

cell.background_color = self.background_color

#==============================

import ui
from ListDataSource import ListDataSource

t = ui.TableView()
t.background_color = 'black'
t.tint_color = 'white'
#l = ui.ListDataSource(['One', 'Two'])
l = ListDataSource(['One', 'Two'])
l.text_color = 'cyan'
l.highlight_color = 'blue'
l.background_color = 'red'
l.tint_color = 'green'
t.data_source = l
t.present()

#==============================


# coding: utf-8

import ui

class MyListDataSource(ui.ListDataSource):
	def __init__(self, items, *args, **kwargs ):
		ui.ListDataSource.__init__(self, items, *args, **kwargs)
		
		
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 1
		
	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return len(tableview.data_source.items)
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		
		# to get different cell types, pass subtitle or value1, or value2
		# to ui.TableViewCell() pass in as a string
		cell = ui.TableViewCell()
		cell.text_label.text = 'Foo Bar'
		if row % 2:
			cell.text_label.text_color = 'purple'
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
if __name__ == '__main__':
	f = (0,0,500,500)
	v = ui.View(frame = f)
	tb = ui.TableView()
	tb.flex = 'wh'
	tb.frame = v.bounds
	tb.data_source = MyListDataSource(range(30))
	v.add_subview(tb)
	v.present('sheet')
	
#==============================

import ui

def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		
		# to get different cell types, pass subtitle or value1, or value2
		# to ui.TableViewCell() pass in as a string
	cell = ui.TableViewCell()
	
	cell.content_view.bg_color = None
	cell.content_view.alpha = 1
	cell.bg_color = 'red'
	
	cell.text_label.text = 'Foo Bar'
	if row % 2:
		cell.text_label.text_color = 'purple'
		
	return cell
	
	
l = ui.ListDataSource(items = range(30))
l.tableview_cell_for_row = tableview_cell_for_row

