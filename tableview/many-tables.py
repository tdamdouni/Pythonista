# Pythonista Forum - @Phuket2

# https://forum.omz-software.com/topic/3576/beginner-help-on-tableview-in-ui-module/10

import ui

class MyClass(ui.View):
	def __init__(self, num_tables=4, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.make_view(num_tables)
		
	def make_view(self, num_tables):
		for i in range(0, num_tables):
			tbl = ui.TableView(name='tbl_' +str(i))
			#tbl.width = self.width / num_tables
			#tbl.height = self.height
			#tbl.x = tbl.width * i
			tbl.data_source = ui.ListDataSource(items=range(40))
			#tbl.flex = 'tlwhbr'
			self.add_subview(tbl)
			
	def layout(self):
		# Layout is called automatically by the ui Module, for Custom
		# ui.Views (aka, classes that subclass ui.View) is only called
		# when a views frame/bounds change.
		
		# get a list of tbls that are subviews. This case we only have
		# ui.TableViews as subviews, but we could also have others, such
		# as buttons, other ui.Views etc...
		tbls = [tbl for tbl in self.subviews if type(tbl) is ui.TableView]
		
		w = self.width / len(tbls)
		h = self.height
		
		for i, tbl in enumerate(tbls):
			tbl.width = w
			tbl.height = h
			tbl.x = i * w
			
if __name__ == '__main__':
	w, h = 600, 800
	f = (0, 0, w, h)
	style = 'sheet'
	
	mc = MyClass(num_tables=6,frame=f, bg_color='white', name='Tables')
	mc.present(style=style, animated=False)
	
	# access the table by name
	print(mc['tbl_1'])
	print(mc['tbl_2'].data_source)

