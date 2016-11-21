# https://forum.omz-software.com/topic/3515/lab-uifiles-referencing-other-uifiles-when-loaded-as-custom-ui-objects

import ui, editor
from random import choice

'''
    Pythonista Forum - @Phuket2
'''

_themes = ['Dawn', 'Tomorrow', 'Solarized Light',
'Solarized Dark', 'Cool Glow', 'Gold', 'Tomorrow Night', 'Oceanic',
'Editorial']

def pyui_bindings(obj):
	# JonB
	def WrapInstance(obj):
		class Wrapper(obj.__class__):
			def __new__(cls):
				return obj
		return Wrapper
		
	bindings = globals().copy()
	bindings[obj.__class__.__name__]=WrapInstance(obj)
	return bindings
	
class UIFileBase(ui.View):
	def __init__(self, ui_file, *args, **kwargs):
		ui.load_view(ui_file, pyui_bindings(self))
		super().__init__(*args, **kwargs)
		
	def add(self, p):
		# do like this so we can add transformations here later
		p.add_subview(self)
		
class Panel(UIFileBase):
	def __init__(self, ui_file = None, *args, **kwargs):
		# hmmm, when a pyui file references this class
		# what comes first, the chicken or the egg?
		if not ui_file:
			ui_file = 'title_panel' # horrible, a constant here
		super().__init__(ui_file, *args, **kwargs)
		print('in Panel')
		
class Combo(UIFileBase):
	# composite of other UIFiles
	def __init__(self, ui_file=None, *args, **kwargs):
		super().__init__(ui_file, *args, **kwargs)
		
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
if __name__ == '__main__':
	_use_theme = True
	w, h = 400, 400
	f = (0, 0, w, h)
	
	ui_file = 'title_panel'
	style = 'sheet'
	animated = False
	
	mc = MyClass(ui_file, frame=f, bg_color='white')
	
	if not _use_theme:
		mc.name = 'No Theme'
		mc.present(style = style, animated=animated)
	else:
		theme = choice(_themes)
		mc.name = theme
		editor.present_themed(mc, theme_name=theme, style=style, animated=animated)
	'''
	pf = ui.Rect(*mc.bounds.inset(20, 20))
	pf.height = 150
	v = Panel(ui_file, frame = pf )
	v.add(mc)
	'''
	ui_file = 'comp'
	pf = ui.Rect(*mc.bounds.inset(5, 5))
	p = Combo(ui_file, frame = pf)
	p.add(mc)
# --------------------

