# coding: utf-8

# Captured from: _https://forum.omz-software.com/topic/2513/getting-the-parent-of-a-dynamically-method-as-a-function/11_

import ui

def test_func(msg):
	'''
	i would like to get a reference to the caller here
	being the btn.
	i am pretty sure the answer lies with the inspect module,
	but i cant figure it out.
	MAYBE, its even easier than that... well that would be great
	'''
	print msg
	
	
btn = ui.Button()
btn.msg = test_func
btn.msg('I am on to something...')

###==============================

import ui

def extra_function(self, message):
	print 'My class: ', self.__class__
	print message
	
b = ui.Button()
b.extra_function = lambda *a, **kw: extra_function(b, *a, **kw)

b.extra_function('The message')

###==============================

import ui

def test_func(obj, msg):
	'''
	i would like to get a reference to the caller here
	being the btn.
	i am pretty sure the answer lies with the inspect module,
	but i cant figure it out.
	MAYBE, its even easier than that... well that would be great
	'''
	print msg
	print obj.title
	
btn = ui.Button(title = 'help')
btn.msg = test_func
btn.msg(btn, 'I am on to something...')

###==============================

import types
btn.msg = types.MethodType(test_func, btn)

###==============================

from functools import partial
btn.msg = partial(test_func, btn)

###==============================

	for k,v in _extended_methods.iteritems():
		setattr(ctl, k, types.MethodType(v, ctl))
		#ctl. = types.MethodType(v, ctl)

