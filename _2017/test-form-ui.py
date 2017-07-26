# https://forum.omz-software.com/topic/4219/how-to-break-out-of-loop-using-ui-button/6

import ui

class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.make_view()
		
	def make_view(self):
		btn = ui.Button(frame=(10, 10, 80, 32),
		bg_color = 'white',
		border_width=.5,
		corner_radius=3,
		action=self.button_hit)
		btn.title = 'Close'
		self.add_subview(btn)
		
	def button_hit(self, sender):
		self.close()
		
if __name__ == '__main__':
	v = MyClass(frame = (0, 0, 300, 400), bg_color='teal', name='Test Form')
	v.present(style='sheet')

