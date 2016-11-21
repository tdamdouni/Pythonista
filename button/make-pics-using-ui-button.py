# https://forum.omz-software.com/topic/3462/lab-easy-way-to-make-pics-using-ui-button/4

'''
    Pythonista Forum - @Phuket2
'''
import ui, editor
import calendar

def btn_image(text, w = 256, *args, **kwargs):
	btn = ui.Button( title = text)
	btn.frame = (0, 0, w, w)
	btn.bg_color = 'teal'
	btn.tint_color = 'white'
	btn.font = ('Arial Rounded MT Bold', w * .4)
	btn.corner_radius = btn.width / 2
	for k, v in kwargs.items():
		if hasattr(btn, k):
			setattr(btn, k, v)
			
	with ui.ImageContext(w, w) as ctx:
		btn.draw_snapshot()
		return ctx.get_image()
		
class MonthDataSource(ui.ListDataSource):
	def __init__(self, items = [], *args, **kwargs):
		lst = []
		for m in range(1, 13):
			rec = dict(title = calendar.month_name[m] , image=btn_image(calendar.month_abbr[m][0], w = 26, bg_color = 'deeppink'), accessory_type = 'checkmark' )
			lst.append(rec)
		items = lst
		super().__init__(items, *args, **kwargs)
		
class TableBase(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.tv = ui.TableView(name='table')
		self.tv.flex = 'wh'
		self.add_subview(self.tv)
		
class MonthTable(TableBase):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.tv.data_source = MonthDataSource()
		
	def layout(self):
		if self.superview:
			self.frame = self.superview.bounds
			
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
if __name__ == '__main__':
	_use_theme = True
	w, h = 300, 600
	f = (0, 0, w, h)
	
	mc = MyClass(frame=f, bg_color='white', name='Months')
	mc.add_subview(MonthTable())
	
	if not _use_theme:
		mc.present('sheet', animated=False)
	else:
		editor.present_themed(mc, theme_name='Oceanic', style='sheet', animated=False)

