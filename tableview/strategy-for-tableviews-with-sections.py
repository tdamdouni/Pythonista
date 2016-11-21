# coding: utf-8

# https://forum.omz-software.com/topic/2234/strategy-for-tableviews-with-sections

import ui

class MyTableViewDataSource (object):
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 0
		
	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		#print section
		return 0
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		print 'cell name: ', row
		cell.text_label.text = row
		return cell
		
	def tableview_title_for_header(self, tableview, section):
		# Return a title for the given section.
		# If this is not implemented, no section headers will be shown.
		print 'section: ', section
		return section
		
	def tableview_can_delete(self, tableview, section, row):
		# Return True if the user should be able to delete the given row.
		return False
		
	def tableview_can_move(self, tableview, section, row):
		# Return True if a reordering control should be shown for the given row (in editing mode).
		return False
		
	def fill_data(self, tableview, data):
		for section in data:
			self.tableview_title_for_header(tableview, section)
			for row in data[section]:
				self.tableview_cell_for_row(tableview, section, row)
				
				
multi_section = ui.TableView()
multi_section.width = 400
multi_section.height = 400

list = {'Header1': ['element1', 'element2', 'element3'], 'Header2': ['element3', 'element4', 'element5'], 'Header3': ['element6', 'element7', 'element8'], 'Header4': ['element9', 'element10']}

data = MyTableViewDataSource()

multi_section.data_source = data
data.fill_data(multi_section, list)

multi_section.present('sheet')

#==============================

def tableview_number_of_sections(self,tableview):
	return len(tableview.data.keys())
def tableview_title_for_header(self,tableview,section):
	return tableview.data.keys()[section]
def tableview_number_of_rows(self,tableview,section):
	key = tableview.data.keys()[section]
	return len(tableview.data[key])
	
#==============================

import ui
from collections import OrderedDict

class MyTableViewDataSource (object):
	def tableview_number_of_sections(self,tableview):
		return len(self.data.keys())
		
	def tableview_title_for_header(self,tableview,section):
		return self.data.keys()[section]
		
	def tableview_number_of_rows(self,tableview,section):
		key = self.data.keys()[section]
		return len(self.data[key])
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		key = self.data.keys()[section]
		cell = ui.TableViewCell()
		cell.text_label.text = self.data[key][row]
		return cell
		
	def fill_data(self, tableview, data):
		self.data = data
		
multi_section = ui.TableView()
multi_section.width = 400
multi_section.height = 400

list = OrderedDict([('Header1', ['element1', 'element2', 'element3']), ('Header2', ['element3', 'element4', 'element5']), ('Header3', ['element6', 'element7', 'element8']), ('Header4', ['element9', 'element10'])])

data = MyTableViewDataSource()

multi_section.data_source = data
data.fill_data(multi_section, list)

multi_section.present('sheet')```
#==============================

print(list((0, 1, 2)))  # works
list = 'a b c'.split()
print(list((0, 1, 2)))  # throws an exception

# coding: utf-8

# https://forum.omz-software.com/topic/2234/strategy-for-tableviews-with-sections

import ui

class MyTableViewDataSource (object):
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 0
		
	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		#print section
		return 0
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		print 'cell name: ', row
		cell.text_label.text = row
		return cell
		
	def tableview_title_for_header(self, tableview, section):
		# Return a title for the given section.
		# If this is not implemented, no section headers will be shown.
		print 'section: ', section
		return section
		
	def tableview_can_delete(self, tableview, section, row):
		# Return True if the user should be able to delete the given row.
		return False
		
	def tableview_can_move(self, tableview, section, row):
		# Return True if a reordering control should be shown for the given row (in editing mode).
		return False
		
	def fill_data(self, tableview, data):
		for section in data:
			self.tableview_title_for_header(tableview, section)
			for row in data[section]:
				self.tableview_cell_for_row(tableview, section, row)
				
				
multi_section = ui.TableView()
multi_section.width = 400
multi_section.height = 400

list = {'Header1': ['element1', 'element2', 'element3'], 'Header2': ['element3', 'element4', 'element5'], 'Header3': ['element6', 'element7', 'element8'], 'Header4': ['element9', 'element10']}

data = MyTableViewDataSource()

multi_section.data_source = data
data.fill_data(multi_section, list)

multi_section.present('sheet')

# *****

def tableview_number_of_sections(self,tableview):
	return len(tableview.data.keys())
def tableview_section_title(self,tableview,section):
	return tableview.data.keys()[section]

