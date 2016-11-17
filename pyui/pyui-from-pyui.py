import ui

# https://forum.omz-software.com/topic/3176/use-a-pyui-file-in-another-pyui-file/9

# wrapper.py, Pythonista Forum @JonB
# https://forum.omz-software.com/topic/3176/use-a-pyui-file-in-another-pyui-file
# remember to add the the name of the class to the 'Custom View Class'
# in the .pyui

_pyui_file_name = 'find.pyui'


def WrapInstance(obj):
	class Wrapper(obj.__class__):
		def __new__(cls):
			return obj
	return Wrapper
	
	
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		ui.load_view(_pyui_file_name,
		bindings={'MyClass': WrapInstance(self), 'self': self})
		
		super().__init__(*args, **kwargs)
		
if __name__ == '__main__':
	w = 600
	h = 325
	f = (0, 0, w, h)
	mc = MyClass(bg_color='deeppink')
	mc.present('sheet')

