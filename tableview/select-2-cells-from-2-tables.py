#!python3

# https://forum.omz-software.com/topic/3576/beginner-help-on-tableview-in-ui-module/2

# simple table
import ui

def cell_tapped1(sender):
	cellval1 = ds1.selected_row + 1
	print ('Maha', cellval1)
	
tv1 = ui.TableView()
tv1.frame = (0,0,95,300)
tv1.width, tv1.height = 95, 270
tv1.row_height = 30
ds1 = ui.ListDataSource(['Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury', 'Ketu','Venus' ])
ds1.action = cell_tapped1
tv1.data_source = tv1.delegate = ds1

def cell_tapped2(sender):
	cellval2 = ds2.selected_row + 1
	print ('Antar',cellval2)
tv2 = ui.TableView()
tv2.frame = (95,0,95,300)
tv2.width, tv2.height = 95, 270
tv2.row_height = 30
ds2 = ui.ListDataSource(['Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury', 'Ketu','Venus' ])
ds2.action = cell_tapped2
tv2.data_source = tv2.delegate = ds2

# Custom ui Class
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.table1_selection = None
		self.bg_color = 'lightyellow'
		self.make_view()
		
	def make_view(self):
		self.add_subview(tv1)
		self.add_subview(tv2)
		tv1.data_source.action = self.tv1_action
		
	def tv1_action(self, sender):
		self.table1_selection = sender.items[sender.selected_row]
		print(self.table1_selection)
		
	# the ui module calls this method automatically, if its definded
	# there are other callbacks you can see them in the help file
	def will_close(self):
		print('view closing...Selection = ', self.table1_selection)
		
f=(0, 0, 300, 480)
#v = ui.View(frame=f)
v = MyClass(name='Tables', frame=f)
#v.name = 'Tables'
#v.background_color = "lightyellow"

#v.add_subview(tv1)
#v.add_subview(tv2)
v.present('sheet')

