# https://forum.omz-software.com/topic/3113/share-a-skeleton-for-making-and-testing-variable-height-cells-for-a-scrollview/25

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

