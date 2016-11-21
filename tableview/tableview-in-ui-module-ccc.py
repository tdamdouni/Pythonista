# https://forum.omz-software.com/topic/3576/beginner-help-on-tableview-in-ui-module/5

# @ccc

# Two simple tables

import ui

neighbors = 'Sun Moon Mars Rahu Jupiter Saturn Mercury Ketu Venus'.split()


class TwoTablesView(ui.View):
	def __init__(self, name='Two Tables', bg_color='lightyellow'):
		self.name = name
		self.bg_color = bg_color
		self.user_data = {}
		self.add_subview(self.make_table_view('Maha', (0, 0, 95, 300)))
		self.add_subview(self.make_table_view('Antar', (95, 0, 95, 300)))
		self.present()
		
	def make_table_view(self, name, frame):
		table_view = ui.TableView(name=name, frame=frame)
		table_view.row_height = 30
		data_source = ui.ListDataSource(neighbors)
		data_source.name = name
		data_source.action = self.table_action
		table_view.data_source = table_view.delegate = data_source
		return table_view
		
	def table_action(self, sender):
		self.user_data[sender.name] = sender.items[sender.selected_row]
		
	def will_close(self):
		print(self.user_data)
		
		
TwoTablesView()

