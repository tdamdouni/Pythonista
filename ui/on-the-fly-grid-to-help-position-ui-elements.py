# https://forum.omz-software.com/topic/3558/lab-on-the-fly-grid-to-help-position-ui-elements/3

# Pythonista Forum - @Phuket2
import ui, editor

def grid_rc_(bounds, rows=1, columns=1):
	# a grid based on rows and columns
	# return a list of lists of ui.Rects
	r = ui.Rect(*bounds)
	w = r.width / columns
	h = r.height / rows
	rl = []
	for i in range(rows):
		lst = []
		for j in range(columns):
			lst.append(ui.Rect(j*w, h*i, w, h))
		rl.append(lst)
	return rl
	
	
def grid_wh_(bounds, w, h):
	# a grid based on widths and heights
	# return a list of lists of ui.Rects
	r = ui.Rect(*bounds)
	
	rl = []
	for i in range(int(r.height / h)):
		lst = []
		for j in range(int(r.width / w)):
			lst.append(ui.Rect(j*w, h*i, w, h))
		rl.append(lst)
	return rl
	
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# create the grids... static here. easy to call adhoc anytime,
		# on any rect to give you a grid as per the params
		self.grid_rc = grid_rc_(self.bounds, rows=3, columns=9)
		self.grid_wh = grid_wh_(self.bounds, w=10, h=10)
		
	def draw(self):
		rc = self.grid_rc
		wh = self.grid_wh
		
		# using row, column grid
		ui.set_color('teal')
		s = ui.Path.rect(*rc[0][8])
		s.fill()
		
		s = ui.Path.rect(*rc[1][0])
		s.fill()
		
		s = ui.Path.rect(*rc[2][4])
		s.fill()
		
		# using wh grid
		ui.set_color('red')
		s = ui.Path.rect(*wh[5][20])
		s.fill()
		
		s = ui.Path.rect(*wh[0][0])
		s.fill()
		
if __name__ == '__main__':
	_use_theme = True
	w, h = 600, 800
	f = (0, 0, w, h)
	style = 'sheet'
	
	mc = MyClass(frame=f, bg_color='white')
	
	if not _use_theme:
		mc.present(style=style, animated=False)
	else:
		editor.present_themed(mc, theme_name='Oceanic', style=style, animated=False)
		
# --------------------
def flattened_list(lst):
	# flatten the list array, the code from stackoverflow
	return [item for sublist in lst for item in sublist]
# --------------------
# Pythonista Forum - @Phuket2
import ui, editor

def grid_rc_(bounds, rows=1, columns=1):
	# a grid based on rows and columns
	# return a list of lists of ui.Rects
	r = ui.Rect(*bounds)
	w = r.width / columns
	h = r.height / rows
	rl = []
	for i in range(rows):
		lst = []
		for j in range(columns):
			lst.append(ui.Rect(j*w, h*i, w, h))
		rl.append(lst)
	return rl
	
def flattened_list(lst):
	# flatten the list array, the code from stackoverflow
	return [item for sublist in lst for item in sublist]
	
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.make_view()
		
	def make_view(self):
		rows = 10
		cols = 5
		
		# get a flatten lst of the specified grid
		lst = flattened_list(grid_rc_(self.bounds, rows, cols))
		
		for i, r in enumerate(lst):
			r = ui.Rect(*r.inset(5, 5))
			btn = ui.Button(name=str(i), frame=r)
			btn.title = str(i)
			btn.border_width = .5
			btn.corner_radius = btn.width * .1
			btn.action = self.btn_action
			self.add_subview(btn)
			
	def btn_action(self, sender):
		print('btn -', sender.name)
		
if __name__ == '__main__':
	_use_theme = False
	w, h = 600, 800
	f = (0, 0, w, h)
	style = 'sheet'
	
	mc = MyClass(frame=f, bg_color='white')
	
	if not _use_theme:
		mc.present(style=style, animated=False)
	else:
		editor.present_themed(mc, theme_name='Oceanic', style=style, animated=False)
		
# --------------------
# Pythonista Forum - @Phuket2
import ui, editor

def grid_rc_(bounds, rows=1, columns=1):
	# a grid based on rows and columns
	# return a list of lists of ui.Rects
	r = ui.Rect(*bounds)
	w = r.width / columns
	h = r.height / rows
	rl = []
	for i in range(rows):
		lst = []
		for j in range(columns):
			lst.append(ui.Rect(j*w, h*i, w, h))
		rl.append(lst)
	return rl
	
def flattened_list(lst):
	# flatten the list array, the code from stackoverflow
	return [item for sublist in lst for item in sublist]
	
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.make_view()
		
	def make_view(self):
		rows = 20
		cols = 15
		# another way, its a little crazy...but maybe @ccc likes it :)
		[self.add_subview(self.create_ui_obj(ui.Button,
		name=str(i),frame=f.inset(5,5), border_width=.5,
		corner_radius= 12, title=str(i), action = self.btn_action,
		bg_color='teal', tint_color='white'))
		for i, f in enumerate(flattened_list(grid_rc_(self.bounds,
		rows, cols)))]
		
		
	def create_ui_obj(self, ui_type, **kwargs):
		obj = ui_type()
		for k, v in kwargs.items():
			if hasattr(obj, k):
				setattr(obj, k, v)
		return obj
		
	def btn_action(self, sender):
		print('btn -', sender.name)
		
if __name__ == '__main__':
	_use_theme = False
	w, h = 600, 800
	f = (0, 0, w, h)
	style = 'sheet'
	
	mc = MyClass(frame=f, bg_color='white')
	
	if not _use_theme:
		mc.present(style=style, animated=False)
	else:
		editor.present_themed(mc, theme_name='Oceanic', style=style, animated=False)
# --------------------
	def make_view(self):
		rows = 20
		cols = 15
		# another way, its a little crazy...but maybe @ccc likes it :)
		[self.add_subview(self.create_ui_obj(ui.Button,
		name=str(i),frame=f.inset(5,5), border_width=.5,
		corner_radius= 6, title=str(i), action = self.btn_action,
		bg_color='maroon', tint_color='white', flex='tlbrwh'))
		for i, f in enumerate(flattened_list(grid_rc_(self.bounds, rows, cols)))]
# --------------------

