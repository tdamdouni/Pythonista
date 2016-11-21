# coding: utf-8

# https://forum.omz-software.com/topic/3176/use-a-pyui-file-in-another-pyui-file/10

import ui
import os

class PYUILoaderStr(ui.View):
	'''
	loads a pyui file into the class, acts as another ui.View
	class.
	** Please note that the pyui class must have its
	Custom Class attr set to selfwrapper
	
	Thanks @JonB
	'''
	def __init__(self, pyui_str, raw = True):
	
		# black magic here, for me at least...
		class selfwrapper(ui.View):
			def __new__(cls):
				return self
				
			if raw:
				pyui_str = json.dumps(pyui_str)
				
			ui.load_view_str(pyui_str,
			bindings={'selfwrapper':selfwrapper, 'self':self})
			
def xx():
	print 'hi'
	return True
	
class PYUILoader(ui.View):
	'''
	loads a pyui file into the class, acts as another ui.View
	class.
	** Please note that the pyui class must have its
	Custom Class attr set to selfwrapper
	
	Thanks @JonB
	'''
	def __init__(self, f_name = None):
		print 'in PYUILoader init'
		
		# black magic here, for me at least...
		class selfwrapper(ui.View):
			def __new__(cls):
				return self
				
		if not f_name.endswith('.pyui'):
			f_name += '.pyui'
			
		# make sure the file exists
		if not os.path.isfile(f_name):
			raise OSError
			
		ui.load_view( f_name ,
		bindings={'selfwrapper':selfwrapper, 'self':self})
		
		
		
class MyClass(PYUILoader):
	def __init__(self, f_name ):
		PYUILoader.__init__(self, f_name)
		self.width = 500
		self.height = 500
		print 'in Myclass'
		self['menu'].bg_color = 'red'
		
	def xx(self):
		print 'hello from my class'
		return True
		
		
		
if __name__ == '__main__':
	mc = MyClass('StdView')
	mc.present('sheet', animated = False)
# --------------------
		v = ViewClass()
	v.frame = _str2rect(view_dict.get('frame'))
	v.flex = attrs.get('flex', '')
	v.alpha = attrs.get('alpha', 1.0)
	v.name = attrs.get('name')
		...
		return v
...
# --------------------
# wrapper.py
def WrapInstance(obj):
	class Wrapper(obj.__class__):
		def __new__(cls):
			return obj
	return Wrapper
	
#MyView.py
from wrapper import WrapInstance
class MyView(ui.View):
	def __init__(self):
		ui.load_view('MyView',bindings={'MyView':WrapInstance(self),'self':self})
# --------------------
import ui

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
# --------------------
ui.load_view(_pyui_file_name,
        bindings={self.__class__.__name__: WrapInstance(self), 'self': self})
# --------------------

def pyui_bindings(obj):
	def WrapInstance(obj):
		class Wrapper(obj.__class__):
			def __new__(cls):
				return obj
		return Wrapper
		
	bindings = globals().copy()
	bindings[obj.__class__.__name__]=WrapInstance(obj)
	return bindings
	
class PYUIClass(ui.View):
	def __init__(self, pyui_fn, *args, **kwargs):
		ui.load_view(pyui_fn, pyui_bindings(self))
		super().__init__(*args, **kwargs)

