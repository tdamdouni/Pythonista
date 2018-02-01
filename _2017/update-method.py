# https://forum.omz-software.com/topic/4199/new-update-method-in-beta-just-curious

import ui
import types


def auto_button(time_out_secs=1, *args, **kwargs):
	'''
	Incomplete attempt at getting something other than a Custom View
	to have its own update event
	'''
	btn = None
	
	def myupdate():
		'''
		here we might change the btns title in x secs. Could then call the
		btn's action. eg, might close a view that is blocked by ui.wait_modal.
		'''
		print('In Update')
		
	btn = ui.Button(**kwargs)
	btn.update = types.MethodType(myupdate, btn)
	btn.update_interval = 1
	return btn
	
	
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.make_view()
		
	def make_view(self):
		btn = auto_button(title='Continue',
		width=100,
		height=32,
		bg_color='white',
		corner_radius=6,
		)
		btn.center = self.center
		self.add_subview(btn)
		
		
if __name__ == '__main__':
	f = (0, 0, 300, 400)
	v = MyClass(frame=f, bg_color='teal')
	v.present(style='sheet')

