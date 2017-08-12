# https://forum.omz-software.com/topic/4232/idea-with-decorators-well-maybe/2

import ui, editor
import inspect
from functools import wraps

#from inspect import formatargspec, getfullargspec

def args_annotation_decorator(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		#ln = inspect.currentframe().f_back.f_lineno
		#ln = inspect.currentframe().f_lineno
		'''
		i tried to get the right line number...it didnt work it out. i am sure its possible,
		i hard coded in just for the sake of showing the raw idea
		'''
		editor.annotate_line(22, str(inspect.currentframe().f_locals))
		return func(*args, **kwargs)
		
	return wrapper
	
@args_annotation_decorator
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.make_view()
		
	def make_view(self):
		pass
		
if __name__ == '__main__':
	f = (0, 0, 300, 400)
	v = MyClass(frame = f)
	v.present(style='sheet', animated=False)
# --------------------
