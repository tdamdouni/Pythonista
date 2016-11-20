# https://forum.omz-software.com/topic/3632/ui-centering/8

# Pythonista Forum - @Phuket2
import ui

class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.make_view()
		
	def make_view(self):
		btn = ui.Button(name='my_btn', frame=(20, 20, 100, 32))
		btn.border_width = .5
		btn.title = 'hello'
		btn.bg_color = 'orange'
		btn.corner_radius = 6
		btn.tint_color = 'white'
		#btn.center = self.bounds.center()
		#btn.flex = 'lrtb'
		self.add_subview(btn)
		
	def layout(self):
		self['my_btn'].center = self.bounds.center()
		
		
if __name__ == '__main__':
	w, h = 330, 600
	f = (0, 0, w, h)
	style = 'sheet'
	
	mc = MyClass(frame=f, bg_color='white')
	mc.present(style=style, animated=False)

