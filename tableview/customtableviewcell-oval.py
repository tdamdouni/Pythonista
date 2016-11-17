# https://gist.github.com/jsbain/c5e7bad33643895c0f0db5e30c97df3a

# https://forum.omz-software.com/topic/3297/ui-tableviewcell-returning-a-custom-class-instead/5

import ui

class CustomTableViewCell(ui.View):
	def as_cell(self):
		c=ui.TableViewCell()
		self.frame=c.content_view.bounds
		self.flex='wh'
		c.content_view.add_subview(self)
		c.set_needs_display()
		return c
	def __init__(self,color):
		self.color=color
	def draw(self):
		path=ui.Path.oval(0,0,self.width,self.height)
		ui.set_color(self.color)
		path.fill()
		
		
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
			cell = CustomTableViewCell('red').as_cell()
		else:
			cell = CustomTableViewCell('blue').as_cell()
			
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

