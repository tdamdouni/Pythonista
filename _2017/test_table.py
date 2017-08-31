# https://gist.github.com/Phuket2/28389804650473cccd2d40e78a6b05a1

import ui
from random import choice


_color_list = ['purple', 'orange', 'deeppink', 'lightblue', 'cornflowerblue'
               'red', 'yellow', 'green', 'pink', 'navy', 'teal', 'olive',
               'lime', 'maroon', 'aqua', 'silver', 'fuchsia',
               ]


class MyCustomCell(ui.View):
	def __init__(self, parent, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.cell = parent
		self.tableview = None
		self.blink_count = 0
		self.lb = None
		self.frame = self.cell.frame
		self.flex = 'wh'
		self.width -= 10
		self.x = 5
		self.height -= 10
		self.y = 5
		self.alpha = .5
		self.corner_radius = 6
		
		# this allows the touch events to pass through my subview
		self.touch_enabled = False
		
		self.update_interval = .2
		
		lb = ui.Label(frame=(0, 0, 24, 24), bg_color='black',
		text_color='white', alignment=ui.ALIGN_CENTER)
		
		lb.center = self.center
		lb.corner_radius = 12
		
		self.lb = lb
		self.add_subview(lb)
		
	def rect_onscreen(self):
		'''
		Have to write this method.  Would be nice if this was built in.
		like ui.TableView.is_visible for example.  I know its just some rect
		math, but it means you need to save extra references etc.. to calculate
		it yourself.
		'''
		return True
		
	def update(self):
		if not self.tableview:
			return
			
		# I did implement this yet. A little drunk and having a party today.
		# but gives the idea...
		if not self.rect_onscreen():
			return
			
		if self.blink_count == 98:
			self.update_interval = 0
			
		self.blink_count += 1
		self.lb.text = str(self.blink_count)
		self.bg_color = choice(_color_list)
		
		
def create_cell():
	'''
	Create and return a ui.TableViewCell. We add a custom ui.View to
	the TableViewCell.content_view. This means our view is sitting on top
	of the normal TableViewCell contents. All is still there.
	Also create an attr in the cell at runtime that points to our custom class.
	I guess this can be done many ways.  I choose this way for the example.
	To me its at least clear for access.
	'''
	cell = ui.TableViewCell()
	myc = MyCustomCell(cell)
	cell.content_view.add_subview(myc)
	cell.my_cell = myc
	return cell
	
	
class MyDataSource(object):

	def __init__(self, data):
		self.data = data
		self.sel_item = 0
		self.cells = [create_cell()
		for _ in range(len(self.data))]
		
	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return len(self.data)
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = self.cells[row]
		cell.text_label.text = self.data[row]
		
		# just showing we can access our class from the my_cell attr
		# we added. In this case I want to save the tableview attr
		cell.my_cell.tableview = tableview
		return cell
		
	def tableview_did_select(self, tableview, section, row):
		# Called when a row was selected.
		self.select_row(row)
		
	def select_row(self, sel_row):
		for cell in self.cells:
			cell.accessory_type = ""
			
		self.cells[sel_row].accessory_type = 'checkmark'
		self.sel_item = sel_row
		
		
def get_table(items):
	tbl = ui.TableView(frame=(0, 0, 300, 400))
	tbl.data_source = MyDataSource(items)
	tbl.delegate = tbl.data_source
	return tbl
	
	
if __name__ == '__main__':
	v = get_table(['Ian', 'Fred', 'John', 'Paul', 'Gaew', 'Pete',
	'Ole', 'Christian', 'Mary', 'Susan', 'Juile'
	'Simone', 'Terry', 'Michael', 'James'])
	v.present(style='sheet', animated=False)

