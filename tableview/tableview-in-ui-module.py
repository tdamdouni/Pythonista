# https://forum.omz-software.com/topic/3576/beginner-help-on-tableview-in-ui-module

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

v = ui.View()
v.name = 'Tables'
v.background_color = "lightyellow"

v.add_subview(tv1)
v.add_subview(tv2)
v.present('sheet')# --------------------

