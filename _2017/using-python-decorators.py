# https://forum.omz-software.com/topic/4232/idea-with-decorators-well-maybe/2

import ui
from functools import wraps
import dialogs

def debug_ui(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		lst = sorted([d for d in vars(func).keys()])
		result = dialogs.list_dialog(title=func.__qualname__, items=lst)
		
		return func(*args, **kwargs)
		
	return wrapper
	
@debug_ui
def make_button(*args, **kwargs):
	pass
	
@debug_ui
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.tb = None
		self.make_view()
		
	def make_view(self):
		make_button()
		pass
		
	def __repr__(self):
		return('Stupid Test Class')
		
if __name__ == '__main__':
	f = (0, 0, 300, 400)
	v = MyClass(frame = f)
	v.present(style='sheet', animated=False)
# --------------------

