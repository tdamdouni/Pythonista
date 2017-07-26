# https://forum.omz-software.com/topic/2234/strategy-for-tableviews-with-sections/10

import ui
from collections import OrderedDict

class MyTableViewDataSource (object):
	def __init__(self, data_dict=None):
		self.data = data_dict
		
	def section_key(self, section):
		#return self.data.keys()[section]
		return list(self.data.keys())[section]
		
	def tableview_number_of_sections(self, tableview):
		return len(self.data)
		
	def tableview_title_for_header(self, tableview, section):
		return self.section_key(section)
		
	def tableview_number_of_rows(self, tableview, section):
		return len(self.data[self.section_key(section)])
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		cell.text_label.text = self.data[self.section_key(section)][row]
		return cell
		
multi_section = ui.TableView()
multi_section.width = multi_section.height = 400

data_dict = OrderedDict((('Header1', ('element0', 'element1', 'element2')),
                         ('Header2', ('element3', 'element4', 'element5')),
                         ('Header3', ('element6', 'element7', 'element8')),
                         ('Header4', ('element9', 'element10'))))

multi_section.data_source = MyTableViewDataSource(data_dict)
multi_section.present('sheet')

