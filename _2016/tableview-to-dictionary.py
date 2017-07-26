# https://forum.omz-software.com/topic/3716/action-on-cell-when-clicked-in-table/3

import ui
import sys

# Create a tableview, with data
self.tv = ui.TableView()
self.tv.row_height = 30
self.tv.data_source = MyTableViewDataSource(self.tv.row_height)
self.tv.delegate = MyTableViewDelegate()

# Update tableview data
self.tv.data_source.items = sorted(self.c.read_vouchers(), key=itemgetter(0), reverse=True)

# Do not allow selection on the TableView
#self.tv.allows_selection = False
self.tv.allows_selection = True

# Add the table
self.add_subview(self.tv)


# Define the class for the Table Data
class MyTableViewDataSource(object):
	def __init__(self, row_height):
		self.row_height = row_height
		self.width = None
		
	def tableview_number_of_rows(self, tableview, section):
		return len(tableview.data_source.items)
		
	def tableview_cell_for_row(self, tableview, section, row):
		self.width, height = ui.get_screen_size()
		cell = ui.TableViewCell()
		cell.bounds = (0, 0, self.width, self.row_height)
		for i in range(3):
			self.make_labels(cell, tableview.data_source.items[row][i], i)
		return cell
		
	def make_labels(self, cell, text, pos):
		label = ui.Label()
		label.border_color = 'lightgrey'
		label.border_width = 0.5
		label.text = str(text)
		if pos == 0:
			label.frame = (self.width*0/5, 0, self.width/5, self.row_height)
		elif pos == 1:
			label.frame = (self.width*1/5, 0, self.width*2/5, self.row_height)
		elif pos == 2:
			label.frame = (self.width*3/5, 0, self.width*2/5, self.row_height)
		label.alignment = ui.ALIGN_CENTER
		cell.content_view.add_subview(label)
		
class MyTableViewDelegate(object):
	@ui.in_background
	def tableview_did_select(self, tableview, section, row):
		select_voucher_index, select_voucher = tableview.data_source.items[row][:2]
		Common().write_config('select_voucher_index', select_voucher_index)
		Common().write_config('select_voucher', select_voucher)
		MyTableView().refresh_last_voucher()

