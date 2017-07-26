# https://forum.omz-software.com/topic/4107/creating-a-pyui-file-that-expands-automatically-on-ipad/2

import ui

class PYUILoader(ui.View):
	# this acts as a normal Custom ui.View class
	# the root view of the class is the pyui file read in
	# code from @JonB
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
		
class MyView(PYUILoader):
	def __init__(self, pyui_fn, *args, **kwargs):
		super().__init__(pyui_fn, *args, **kwargs)
		
if __name__ == '__main__':
	w, h = 600, 800
	f = (0, 0, w, h)
	pyui_file_name ='my_pyui.pyui' # has to be a vaild filename to a UI.File
	'''
	for this code to work, you need to set the 'Custom View Class' property in the pyui
	file to the name of the class. in this case its 'MyView'.
	'''
	
	mc = MyView(pyui_file_name, frame = f, bg_color = 'deeppink')
	mc.present('sheet')

