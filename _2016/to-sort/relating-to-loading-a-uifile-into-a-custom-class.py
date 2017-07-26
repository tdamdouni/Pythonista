# https://forum.omz-software.com/topic/3629/relating-to-loading-a-uifile-into-a-custom-class

import ui

class UserItem(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.make_view()
		print(self.superview)
		
	def make_view(self):
		pass
		
class PYUILoader(ui.View):
	def WrapInstance(obj):
		class Wrapper(obj.__class__):
			def __new__(cls):
				return obj
		return Wrapper
		
	def __init__(self, pyui_fn, *args, **kwargs):
		bindings=globals().copy()
		bindings[self.__class__.__name__]=self.WrapInstance()
		
		ui.load_view(pyui_fn, bindings)
		
		# call after so our kwargs modify attrs
		super().__init__(*args, **kwargs)
		
class MyClass(PYUILoader):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.make_view()
		
	def make_view(self):
		pass
		
if __name__ == '__main__':
	w, h = 600, 800
	f = (0, 0, w, h)
	
	# any UIFile, with a customview added, then for the customview
	# Custom View Class attr = UserItem
	ui_file = 'hcard'
	
	style = 'sheet'
	
	mc = MyClass(ui_file, frame = f, bg_color = 'white')
	mc.present(style=style)
# --------------------

