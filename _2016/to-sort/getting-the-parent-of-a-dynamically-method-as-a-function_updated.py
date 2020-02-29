# coding: utf-8

# https://forum.omz-software.com/topic/2513/getting-the-parent-of-a-dynamically-method-as-a-function/52

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

import types

class Extender(object):
	def __new__(cls, target_instance, *args, **kwargs):
		if isinstance(cls.__init__, types.MethodType):
			cls.__init__.__func__(target_instance, *args, **kwargs)
		extender_instance = super(Extender, cls).__new__(cls)
		for key in dir(extender_instance):
			if key.startswith('__'): continue
			value = getattr(extender_instance, key)
			if callable(value):
				setattr(target_instance, key, types.MethodType(value.__func__, target_instance))
			else:
				setattr(target_instance, key, value)
		return target_instance
#==============================

# coding: utf-8
import ui
from extend import Extender

def MyMother(sender):
	print('I love my Mums cooking')
	
class DefaultStyle(Extender):
	border_width = .5
	corner_radius = 3
	background_color = 'teal'
	tint_color = 'white'
	
class ButtonFactory(Extender):
	def __init__(self, parent = None, position = (0,0), **kwargs):
		if parent: parent.add_subview(self)
		self.size_to_fit()
		(self.x, self.y) = position
		self.width += 10
		self.action = MyMother
		for key, value in kwargs.iteritems():
			setattr(self, key, value)
			
			
view = ui.View(frame = (0,0,500,500))

button = ButtonFactory(
    DefaultStyle(
        ui.Button(title = 'What do I like?')),
    parent = view, tint_color = 'yellow')

view.present('sheet')
#==============================

def copy_obj(obj , **kwargs):
	new_obj = type(obj)()
	# copy the attrs from the passed object to the new object
	
	attr_exclude_list = ['left_button_items', 'right_button_items', 'navigation_view', 'on_screen', 'subviews', 'superview']
	
	# is removed in the list comp because is callable. we add it back :)
	attr_include_list = ['action']
	
	intrested_attrs = [k for k in dir(obj) if not k.startswith('_') and not callable(getattr(obj, k)) and k not in attr_exclude_list ] + attr_include_list
	
	for k in intrested_attrs:
		if hasattr(new_obj, k):
			print(k, getattr(obj, k))
			setattr(new_obj, k, getattr(obj, k))
			
	# overwite new attrs in the new object ,passed in **kwargs
	for k, v in kwargs.iteritems():
		if hasattr(new_obj, k):
			setattr(new_obj, k, v)
			
	return new_obj
	
#==============================

import warnings

def copy_obj(obj , **kwargs):
	# an idea for ui object copying...
	
	# a list of object types we accept
	ui_can_copy = [ui.View, ui.Button, ui.Label, ui.TextField, ui.TextView, ui.TableView, ui.ImageView, ui.SegmentedControl, ui.ScrollView]
	
	if type(obj) not in ui_can_copy:
		warnings.warn('Can not copy object {}'.format(type(obj)))
		return
		
	new_obj = type(obj)()
	# copy the attrs from the passed object to the new object
	
	
	attr_exclude_list = ['left_button_items', 'right_button_items', 'navigation_view', 'on_screen', 'subviews', 'superview', 'content_offset', 'content_size']
	
	# is removed in the list comp because is callable. we add it back :)
	attr_include_list = ['action']
	
	intrested_attrs = [k for k in dir(obj) if not k.startswith('_') and not callable(getattr(obj, k)) and k not in attr_exclude_list ] + attr_include_list
	
	for k in intrested_attrs:
		if hasattr(new_obj, k):
			print(k, type(getattr(obj, k)))
			attr = getattr(obj, k)
			'''
			This is an important test. if we try to copy a string attr
			that has nit been previously set, it will fail if we do
			a blind copy/assignment
			'''
			if attr:
				setattr(new_obj, k, attr)
				
	# overwite new attrs in the new object ,passed in **kwargs
	for k, v in kwargs.iteritems():
		if hasattr(new_obj, k):
			setattr(new_obj, k, v)
			
	return new_obj
	
def test_copy_obj():
	# notice there us No navigation_view also no ui.ButtonItem
	ui_can_copy = [ui.View, ui.Button, ui.Label, ui.TextField, ui.TextView, ui.TableView, ui.ImageView, ui.SegmentedControl, ui.ScrollView]
	
	for obj in ui_can_copy:
		o = obj()
		print(type(o))
		x = copy_obj(o)

