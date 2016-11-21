# https://gist.github.com/Phuket2/f04dee860e85d333f62541eac4f65fed

# https://forum.omz-software.com/topic/3297/ui-tableviewcell-returning-a-custom-class-instead/11

import ui

_colors = ['teal', 'deeppink', 'orange', 'blue', 'red']

class CustomTableViewCell(ui.View):
	'''
	some magic from @JonB see...
	https://forum.omz-software.com/topic/3297/ui-tableviewcell-returning-a-custom-class-instead/4
	'''
	def as_cell(self):
		c=ui.TableViewCell()
		self.frame=c.content_view.bounds
		self.flex='wh'
		c.content_view.add_subview(self)
		c.set_needs_display()
		return c
		
	def __init__(self, tableview, section, row):
		self.tableview = tableview
		self.section = section
		self.row = row
		
	def draw(self):
		x = 0
		for i in range(0, 5):
			r = ui.Rect(x, 0,self.height,self.height).inset(10, 10)
			s=ui.Path.oval(*r)
			ui.set_color(_colors[i])
			s.fill()
			
			if not i:
				r1 = ui.Rect(r.x, r.y, r.width, 22)
				r1.center(r.center())
				r1.x = r.x
				# only draw text on 0 item
				ui.draw_string(str(self.row),
				rect= r1,
				font=('Arial Rounded MT Bold', 22),
				color='white',
				alignment=ui.ALIGN_CENTER,
				line_break_mode=ui.LB_TRUNCATE_TAIL)
				
			x = r.max_x + 3
			
class MyTable(ui.View):
	def __init__(self, items ,  *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.items = items
		self.cv = None
		self.tv = None
		
		self.make_content_view()
		self.make_table()
		
	def make_content_view(self):
		cv = ui.View(frame = self.bounds)
		cv.bg_color = 'orange'
		cv.border_color = 'black'
		cv.corner_radius = 8
		self.cv = cv
		self.add_subview(cv)
		
	def make_table(self):
		tv = ui.TableView(frame = self.cv.bounds)
		tv.flex = 'WH'
		tv.data_source = self
		tv.delegate = self
		tv.separator_color = (0, 0, 0, 0)
		tv.row_height = 88 * 1.4
		self.tv = tv
		self.cv.add_subview(tv)
		
	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return len(self.items)
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = CustomTableViewCell(tableview, section, row).as_cell()
		return cell
		
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.content_view = None
		self.tbl = None
		
		self.make_view()
		
	def make_view(self):
		cv = ui.View(frame=(ui.Rect(0, 0, self.width, self.height - 88)))
		self.add_subview(cv)
		self.content_view = cv
		
		slider = ui.Slider(frame = (0, cv.height + 30, self.width, 32))
		slider.action = self.do_slider
		self.add_subview(slider)
		
	def do_slider(self, sender):
		size_v = tbl.tv.content_size[1]
		tbl.tv.content_offset = (0, size_v * sender.value)
		
		
if __name__ == '__main__':
	w, h = 600, 800
	f = (0, 0, w, h)
	mc = MyClass(frame = f, bg_color = 'white', name = 'Crude Example')
	
	tbl = MyTable(items = range(100000), frame = ui.Rect(*f).inset(10, 10))
	mc.tbl = tbl
	
	mc.content_view.add_subview(tbl)
	mc.present('sheet', animated = False)

