# https://forum.omz-software.com/topic/4294/how-do-i-access-a-gui-element/6

import ui

class PYUILoader(ui.View):
	# this acts as a normal Custom ui.View class
	# the root view of the class is the pyui file read in
	def WrapInstance(obj):
		class Wrapper(obj.__class__):
			def __new__(cls):
				return obj
		return Wrapper
		
	def __init__(self, pyui_fn, *args, **kwargs):
		bindings = globals().copy()
		bindings[self.__class__.__name__] = self.WrapInstance()
		
		ui.load_view(pyui_fn, bindings)
		
		# call after so our kwargs modify attrs
		super().__init__(*args, **kwargs)
		
		
class MyClass(PYUILoader):
	'''
	Just have to be mindful of a few things.
	1. Set your instance vars before the super is called, otherwise
	they will not be accessible in the did_load.
	
	2.  Do any form element setup in the did_load call back. The ui module
	call this method.
	
	3. In the in the UIFile in the 'Custom View Class' section you must
	put in the name of this class. In this case MyClass
	
	4. I like the dict update in the did_load method.  Nothing to do with
	getting this class setup. But its just a quick short cut for setting
	instance vars to your form elms for you can access them with dot notation.
	of course you could have just done self.label1 = self['lablel1'].
	Just a nice short cut.
	'''
	def __init__(self, uifilename, *args, **kwargs):
		self.set_instance_vars_here = 'Yes you got me'
		super().__init__(uifilename, *args, **kwargs)
		
	def did_load(self):
		print(self.set_instance_vars_here)
		
		# add all instance vars for the form elements to the class.
		# its ok, but the late binding means the editor can not help
		# still better than string indexs I think.
		# This is not recursive. It could be though.
		[self.__dict__.update({sv.name: sv}) for sv in self.subviews]
		self['label1'].text = 'My Text'
		self.label1.text = 'My Text'
		
		
if __name__ == '__main__':
	uifilename = 'test1.pyui'
	f = (0, 0, 300, 400)
	v = MyClass(uifilename, frame=f)
	v.present(style='sheet', animated=False)

