# https://gist.github.com/Phuket2/b6a437153bd99538e0b7c852de71b38d

# https://forum.omz-software.com/topic/3386/share-pyui-viewer-class-insertion

import ui, editor

'''
        VERY IMPORTANT
        For the .pyui file to be loaded as you would expect, in the
        ui Designer you have to go to the top level (no obejects sekected),
        you will see a field called 'Custom View Class', you need to enter
        the key that is used for WrapInstance attr that is passed in the
        bindings param to ui.load_view. With the example below you would
        use MyClass.
        bindings={'MyClass': WrapInstance(self), 'self': self})

        The actual name is not important, but they need to match.

        This tweak was made possible by @JonB and @omz for provinding the
        bindings param.

        You can see the thread at
        https://forum.omz-software.com/topic/3176/use-a-pyui-file-in-another-pyui-file
'''

# map the built in theme
_themes =\
        {
                'd' : 'Dawn',
                't' : 'Tomorrow',
                'sl': 'Solarized Light',
                'sd': 'Solarized Dark',
                'cg': 'Cool Glow',
                'g' : 'Gold',
                'tn': 'Tomorrow Night',
                'o' : 'Oceanic',
                'e' : 'Editorial',
        }


def WrapInstance(obj):
	class Wrapper(obj.__class__):
		def __new__(cls):
			return obj
	return Wrapper
	
	
class PYUIViewer(ui.View):
	# this acts as a normal Custom ui.View class
	# the root view of the class is the pyui file read in
	def __init__(self, pyui_fn, *args, **kwargs):
		ui.load_view(pyui_fn,
		bindings={'MyClass': WrapInstance(self), 'self': self})
		
		# call after so our kwargs modify attrs
		super().__init__(*args, **kwargs)
		
if __name__ == '__main__':
	w, h = 600, 600
	f = (0, 0, w, h)
	
	fn = 'icurr.pyui'                       # .pyui file name here
	style = 'sheet'
	theme = _themes['sd']
	
	v = PYUIViewer(fn, frame=f)
	
	editor.present_themed(v,
	theme_name=theme,
	style=style,
	animated=True)

