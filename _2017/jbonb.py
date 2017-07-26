#!python3

# https://gist.github.com/anonymous/5024fc8b3a0562b2d0d4eebffd1246cf

# https://forum.omz-software.com/topic/2234/strategy-for-tableviews-with-sections/11

import ui
from collections import OrderedDict

class MyTableViewDataSource (object):
	def __init__(self, data_dict=None):
		self.data = data_dict
		
	def section_key(self, section):
		#return self.data.keys()[section]
		#return list(self.data.keys())[section]
		return self.data.section_key(section)
		
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


class SectionsDict(OrderedDict):
	'''
	Inherits from OrderedDict
	Simple class to assemble a OrderedDict for use with ui.TableView, when you want a table with sections and data rows.
	'''
	def __init__(self, data_dict = None):
		'''
		params
		data_dict: either an OrderedDict or dict.  expecting a
		string key and a list of strings
		eg. {'header 1':['Listing 1', 'Listing 2', 'Listing 2']}
		'''
		if data_dict:
			self.update(data_dict)
			
	def add_section(self, section, data_list, overwrite=True):
		'''
		Sections, will appear in the order added
		'''
		if overwrite:
			# default behaviour, overwites the section if it exists
			self.update({section:data_list})
		else:
			# append data_list to section, if section exists, otherwise add the section
			sec = self.get(section)
			if sec:
				sec += data_list
			else:
				self.update({section:data_list})
				
	def section_key(self, section_index):
		# can be used to return the section item by index
		return list(self.keys())[section_index]
		
		
s = SectionsDict()
s.add_section('Header1', ['element0', 'element1', 'element2'])
s.add_section('Header2', ['element3', 'element4', 'element5'])
s.add_section('Header3', ['element6', 'element7', 'element8'])
s.add_section('Header4', ['element9', 'element10'])

# also takes a ordered dict, can uncomment the below line
#s = SectionsDict(data_dict)

#multi_section.data_source = MyTableViewDataSource(data_dict)
multi_section.data_source = MyTableViewDataSource(s)

multi_section.present('sheet')

