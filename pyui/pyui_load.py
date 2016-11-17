# coding: utf-8

# https://gist.github.com/Phuket2/c24156294c220668270d

# https://forum.omz-software.com/topic/2534/suggestion-ui-designer

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
			
class PYUILoader(ui.View):
	'''
	loads a pyui file into the class, acts as another ui.View
	class.
	** Please note that the pyui class must have its
	Custom Class attr set to selfwrapper
	
	Thanks @JonB
	'''
	def __init__(self, f_name = None):
	
	
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
		
		
if __name__ == '__main__':
	pass

