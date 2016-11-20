# https://gist.github.com/jsbain/e5004c7ef2f44bba9b6fa7b470d26ba9

# https://forum.omz-software.com/topic/3297/ui-tableviewcell-returning-a-custom-class-instead/5

import ui

#necessary if we want to fool acustomTableViewCell into thinking it is a TableViewCell, mainly for allowing cls.method() type callbacks.
class MockTableCellType(type):
	def __instancecheck__(self, other):
		if other==ui.TableViewCell:
			return True
			
class CustomTableViewCell(object):
	__metaclass__=MockTableCellType
	def __new__(cls,color):
		c=ui.TableViewCell()
		#you can put WHATEVER YOU WANT inside content_view.
		c.content_view.add_subview(ui.View(bg_color=color,frame=c.content_view.bounds))
		c.hello=lambda:cls.hello(c)
		return c
	def hello(self):
		print('hello')
		
class MyTableViewDataSource (object):
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 1
		
	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return 2
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		if row==0:
			cell = CustomTableViewCell('red')
		else:
			cell = CustomTableViewCell('blue')
			
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
t=ui.TableView()
t.frame=(0,0,200,480)
t.data_source=MyTableViewDataSource()
t.present('sheet')

