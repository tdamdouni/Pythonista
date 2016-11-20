# https://forum.omz-software.com/topic/3594/displaying-valid-color-names-in-two-tables

# Aim to display all color names of Pythonista in two tables
# With first table printed color name in white & second in black

import ui

data = 'aliceblue antiquewhite aqua aquamarine azure beige bisque black blanchedalmond blue blueviolet brown burlywood cadetblue chartreuse chocolate coral cornflowerblue cornsilk crimson cyan darkblue darkcyan darkgoldenrod darkgray darkgreen darkgrey darkkhaki darkmagenta darkolivegreen darkorange darkorchid darkred darksalmon darkseagreen darkslateblue darkslategray darkslategrey darkturquoise darkviolet deeppink deepskyblue dimgray dimgrey dodgerblue firebrick floralwhite forestgreen fuchsia gainsboro ghostwhite gold goldenrod gray green greenyellow grey honeydew hotpink indianred indigo ivory khaki lavender lavenderblush lawngreen lemonchiffon lightblue lightcoral lightcyan lightgoldenrodyellow lightgray lightgreen lightgrey lightpink lightsalmon lightseagreen lightskyblue lightslategray lightslategrey lightsteelblue lightyellow lime limegreen linen magenta maroon mediumaquamarine mediumblue mediumorchid mediumpurple mediumseagreen mediumslateblue mediumspringgreen mediumturquoise mediumvioletred midnightblue mintcream mistyrose moccasin navajowhite navy oldlace olive olivedrab orange orangered orchid palegoldenrod palegreen paleturquoise palevioletred papayawhip peachpuff peru pink plum powderblue purple rebeccapurple red rosybrown royalblue saddlebrown salmon sandybrown seagreen seashell sienna silver skyblue slateblue slategray slategrey snow springgreen steelblue tan teal thistle tomato turquoise violet wheat white whitesmoke yellow yellowgreen white'.split()

class MyTableViewDataSource (object):
	def __init__(self, data=None):
		self.data = data
		
	def tableview_number_of_rows(self, tableview, section):
		return len(self.data)
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		cell.text_label.text_color = self.data[-1]
		cell.border_color ='black'
		cell.border_width = 1
		cell.bg_color = self.data[row]
		cell.text_label.alignment = 1
		cell.text_label.font = ('<System-Bold>',18)
		cell.text_label.text = self.data[row]
		return cell
		
size = ui.get_screen_size()
wd,ht = size
view = ui.View()
view.name = 'Color Names'
view.frame =(0,0,wd,ht)
view.background_color ='white'

tv = ui.TableView()
tv.frame = (0,0,wd/2.0,ht)
tv.data_source = MyTableViewDataSource(data)
view.add_subview(tv)

tv1 = ui.TableView()
tv1.frame = (wd/2.0,0,wd/2.0,ht)
# to make text black in 2nd table
data1 = list(data)
data1[-1] = 'black'
tv1.data_source = MyTableViewDataSource(data1)
view.add_subview(tv1)

view.present('sheet')
# --------------------

