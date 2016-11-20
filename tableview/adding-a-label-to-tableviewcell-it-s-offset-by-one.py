# coding: utf-8

# https://forum.omz-software.com/topic/1922/adding-a-label-to-tableviewcell-it-s-offset-by-one/28

import ui

_days = ['Monday', 'Tuesday', 'Wednesday','Thursday', 'Friday', 'Saturday','Sunday']

# the colors corresponding to days of the week
# thai people often wear these colors on the day
# of the week. Is related to the Royal Family.
# Currently, the most important is yellow, the
# The King of Thailand was born on a Monday
# He is the longest severing and living monach
# in the world.
_colors = ['yellow', 'pink', 'green', 'orange', 'blue', 'purple', 'red']


class MyTableViewDataSource (object):
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 1
		
	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return len(_days)
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		cell.text_label.text = _days[row]
		
		# create a label inside the cell
		# the documentation says to add it to the
		# content view
		lb = ui.Label()
		lb.x , lb.y = 15, 30
		lb.width = cell.width - lb.x
		lb.text_color = _colors[row]
		lb.text = _colors[row]
		cell.content_view.add_subview(lb)
		cell.add_subview(lb)
		return cell
		
	def tableview_title_for_header(self, tableview, section):
		# Return a title for the given section.
		# If this is not implemented, no section headers will be shown
		if section == 0:
			return 'Week Days'
			
			
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
	frame = (0,0,540,576)
	v = ui.View()
	tb = ui.TableView()
	tb.frame = frame
	v.add_subview(tb)
	tb.data_source = MyTableViewDataSource()
	v.present('sheet')
# --------------------

