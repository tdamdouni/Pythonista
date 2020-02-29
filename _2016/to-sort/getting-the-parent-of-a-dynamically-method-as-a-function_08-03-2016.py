# coding: utf-8

# https://forum.omz-software.com/topic/2513/getting-the-parent-of-a-dynamically-method-as-a-function/45

from __future__ import print_function
import ui

def test_func(msg):
	'''
	i would like to get a reference to the caller here
	being the btn.
	i am pretty sure the answer lies with the inspect module,
	but i cant figure it out.
	MAYBE, its even easier than that... well that would be great
	'''
	print(msg)
	
	
btn = ui.Button()
btn.msg = test_func
btn.msg('I am on to something...')

#==============================

# coding: utf-8

import types

# Extend the instance given as the first argument with the methods and properties of the instances given as the second and subsequent arguments
def extend(target, *args):
	for source in args:
		for key in dir(source):
			if key.startswith('__'): continue
			value = getattr(source, key)
			if callable(value):
				setattr(target, key, types.MethodType(value.__func__, target))
			else:
				setattr(target, key, value)
	return target
#==============================

# coding: utf-8

import ui
from extend import extend

class DefaultStyle(object):
	background_color = '#fff7ee'
	tint_color = 'black'
	
class HighlightStyle(DefaultStyle):
	def __init__(self):
		super(HighlightStyle, self).__init__()
		self.tint_color = 'red'
		
class ClickHandler(object):
	def __init__(self):
		self.action = self.click_handler
		self.click_color = 'blue'
	def click_handler(self, sender):
		self.tint_color = self.click_color
		
view = ui.View()

button = extend(ui.Button(), HighlightStyle(), ClickHandler())

button.title = 'Styled button'
view.add_subview(button)

view.present()

button.frame = view.bounds.inset(300, 100)

#==============================

import types
import ui

# Extend the instance given as the first argument with the methods and properties of the instances given as the second and subsequent arguments
def extend(target, *args):
	for source in args:
		for key in dir(source):
			if key.startswith('__'): continue
			value = getattr(source, key)
			if callable(value):
				setattr(target, key, types.MethodType(value.__func__, target))
			else:
				setattr(target, key, value)
	return target
	
class DefaultStyle(object):

	background_color = '#fff7ee'
	tint_color = 'black'
	
	def __init__(self):
		self.action = self.click_handler
		self.click_color = 'blue'
		
	def click_handler(self, sender):
		self.tint_color = self.click_color
		
class HighlightStyle(DefaultStyle):
	def __init__(self):
		super(HighlightStyle, self).__init__()
		#DefaultStyle.__init__(self)
		self.tint_color = 'red'
		self.border_width = 1
		self.bg_color = 'yellow'
		self.x = 10
		self.y = 10
		
class MyCustomAttrs(object):
	def __init__(self):
		self.xzy = 666
		
if __name__ == '__main__':
	f = (0,0,500,500)
	v = ui.View(frame = f)
	v.bg_color = 'white'
	
	button = extend(ui.Button(name = 'test'), HighlightStyle(), MyCustomAttrs())
	print(dir(button))
	button.title = 'Styled button'
	button.size_to_fit()
	button.x = 10
	button.y = 10
	button.border_width = .5
	v.add_subview(button)
	print(button.superview)
	
	v.present('sheet')
	
#==============================

# coding: utf-8

import ui

def MyMother(sender):
	print('I love my Mums cooking')
	
_default_btn_style = \
    {
        'border_width' : .5,
        'corner_radius' : 3,
        'bg_color' : 'teal',
        'tint_color' : 'white',
        'action'  : MyMother,
    }

_btn_style = _default_btn_style

_extra_attrs = \
    {
        'myx' : 0,
        'myy' : 0,
    }


def make_button(style = _btn_style, ext_attrs = _extra_attrs ,
                        *args, **kwargs):
	btn = ui.Button()
	
	# process the normal atttrs
	for k,v in kwargs.iteritems():
		if hasattr(btn, k):
			setattr(btn, k, v)
			
	# process a style dict
	for k,v in style.iteritems():
		if hasattr(btn, k):
			setattr(btn, k, v)
			
	# process addtional attrs...
	for k,v in ext_attrs.iteritems():
		setattr(btn, k, v)
		
	# if kwargs has a parent key, then we add the subview to the parent
	if kwargs.has_key('parent'):
		kwargs['parent'].add_subview(btn)
		
	btn.size_to_fit()
	# size to fit is too tight
	btn.frame = ui.Rect(*btn.bounds).inset(0, -5)
	
	return btn
	
if __name__ == '__main__':
	f = (0,0,500,500)
	v = ui.View(frame = f)
	btn = make_button(title = 'What do I Like', parent = v)
	v.present('sheet')
	
#==============================

def test_func(sender):
	return sender
	
v = ui.load_view()
button = v['button1']
button.action = test_func

