# https://forum.omz-software.com/topic/3652/lab-fixed-gridoverlay-class

# Pythonista Forum - @Phuket2

import ui, editor

class FixedGridOverlay(ui.View):
	def __init__(self, parent, rows=1, cols=1, draw=False,
	*args, **kwargs):
	
		super().__init__(*args, **kwargs)
		self.draw_grid = draw
		self.rows = rows if rows else 1
		self.cols = cols if cols else 1
		self.frame = parent.bounds
		self.flex = 'wh'
		self.alpha = .3
		
	def get_fixed_grid(self):
		w = self.width / self.cols
		h = self.height / self.rows
		
		# this list comp, is nice, for me anyway.
		return [ui.Rect(x*w, y*h, w, h) for x in range(self.cols)
		for y in range(self.rows)]
		
	def draw(self):
		# is an attr we can set to True or False
		if not self.draw_grid:
			return
			
		ui.set_color('lightgreen')
		for r in self.get_fixed_grid():
			ui.Path.rect(*r).stroke()
			
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.grid_overlay = FixedGridOverlay(self, rows=40, cols=40,
		draw=True)
		self.add_subview(self.grid_overlay)
		self.make_view()
		
	def make_view(self):
		btn = ui.Button(name='btn', frame=(40, 40, 100, 32))
		btn.title = 'Test Button'
		btn.border_width = 1
		btn.border_color = 'white'
		btn.corner_radius = 8
		btn.action = self.btn_action
		self.add_subview(btn)
		
	def btn_action(self, sender):
		print(sender.title)
		
if __name__ == '__main__':
	_use_theme = True
	w, h = 600, 800
	f = (0, 0, w, h)
	style = 'sheet'
	style = ''
	
	mc = MyClass(name='Grid overlay test', frame=f, bg_color='white')
	
	if not _use_theme:
		mc.present(style=style, animated=False)
	else:
		editor.present_themed(mc, theme_name='Oceanic',
		style=style, animated=False)

