# coding: utf-8

# https://forum.omz-software.com/topic/3269/deleted-row-index-for-listdatasource/3

from __future__ import print_function
import ui

class MyTableViewDataSource (object):
	def __init__(self, row_height):
		self.row_height = row_height
		self.width = None
		
	def tableview_number_of_rows(self, tableview, section):
		return len(tableview.data_source.items)
		
	def tableview_cell_for_row(self, tableview, section, row):
		self.width, height = ui.get_screen_size()
		cell = ui.TableViewCell()
		label = ui.Label()
		label.frame = (0,0,self.width,self.row_height)
		label.border_color = 'red'
		label.border_width = 1
		label.text = tableview.data_source.items[row]
		label.alignment = ui.ALIGN_CENTER
		cell.content_view.add_subview(label)
		return cell
		
	def tableview_can_delete(self, tableview, section, row):
		return True
		
	def tableview_delete(self, tableview, section, row):
		print('Delete row ' + str(row))
		del tableview.data_source.items[row]
		tableview.reload()
		
class MyTableViewDelegate (object):
	def tableview_title_for_delete_button(self, tableview, section, row):
		return 'Delete me'
		
class MyTableView(ui.View):
	def __init__(self):
		self.select_color = 'lightgrey'
		self.unselect_color = 'white'
		self.tv = ui.TableView()
		self.tv.row_height = 50
		self.tv.data_source = MyTableViewDataSource(self.tv.row_height)
		self.all_items = ['1', '2', '3']
		self.tv.data_source.items = self.all_items
		self.name = 'TableView-Test'
		self.tv.delegate = MyTableViewDelegate()
		self.tv.allows_selection = True
		self.add_subview(self.tv)
		self.present('full_screen')
		
	def layout(self):
		self.tv.reload()
		self.tv.frame = (0, 0, self.width, self.height)
		
MyTableView()


