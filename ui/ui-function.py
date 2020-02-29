from __future__ import print_function
# https://forum.omz-software.com/topic/3575/need-help-about-ui-function/4

#!python2

from objc_util import *
import ui

MPicker = ObjCClass('MPMediaPickerController')

def mediaPicker_didPickMediaItems_(_self, _cmd, _mp, _collection):
	picker = ObjCInstance(_mp)
	print('!!!', picker, ObjCInstance(_collection))
	picker.dismissViewControllerAnimated_completion_(True, None)
	
def mediaPickerDidCancel_(_self, _cmd, _mp):
	ObjCInstance(_mp).dismissViewControllerAnimated_completion_(True, None)
	
MediaPickerDelegate = create_objc_class('MediaPickerDelegate', methods=[mediaPicker_didPickMediaItems_, mediaPickerDidCancel_], protocols=['MPMediaPickerDelegate'])
mpDelegate = MediaPickerDelegate.alloc().init()

# Set "pick_music" as the action of a button in "myui.pyui"
def pick_music(sender):
	mp1 = MPicker.alloc().initWithMediaTypes_(1)
	mp1.setDelegate_(mpDelegate)
	mp1.allowsPickingMultipleItems = False
	root_vc = UIApplication.sharedApplication().keyWindow().rootViewController()
	while root_vc.presentedViewController():
		root_vc = root_vc.presentedViewController()
	root_vc.presentViewController_animated_completion_(mp1, True, None)
	
v = ui.load_view('myui')
v.present('sheet')
# --------------------
#Pythonista Forum - @Phuket2
import ui, editor

def pyui_bindings(obj):
	# Pythonista Forum, @JonB
	def WrapInstance(obj):
		class Wrapper(obj.__class__):
			def __new__(cls):
				return obj
		return Wrapper
		
	bindings = globals().copy()
	bindings[obj.__class__.__name__] = WrapInstance(obj)
	return bindings
	
# a Custom ui class as it subclasses ui.View
class MYUIClass(ui.View):
	def __init__(self, ui_file, *args, **kwargs):
		ui.load_view(ui_file, pyui_bindings(self))
		super().__init__(*args, **kwargs)
		ui.View.__init__(self, *args, **kwargs)
		
	# this is a callback from ui, is called automatically for a custom
	# class, if the method is defined
	def will_close(self):
		print('the view will close')
		
	def did_load(self):
		print('the pyui file has loaded...')
		
if __name__ == '__main__':
	_use_theme = True
	w, h = 320, 320
	f = (0, 0, w, h)
	
	ui_file = 'myui'
	style = 'sheet'
	animated = False
	theme = 'Oceanic'
	hide_title_bar = False
	
	mc = MYUIClass(ui_file, frame=f, bg_color='white')
	
	if not _use_theme:
		mc.present('sheet', animated=animated,
		hide_title_bar=hide_title_bar)
	else:
		mc.name = theme
		editor.present_themed(mc, theme_name=theme,
		style=style, animated=animated,
		hide_title_bar=hide_title_bar)
# --------------------

import ui

def mediaPicker_didPickMediaItems_(_self,_cmd,mediaPicker,mediaItemCollection):
	print('!!!',ObjCInstance(mediaPicker),ObjCInstance(mediaItemCollection))
	
mediaPickerDelegate = create_objc_class('mediaPickerDelegate',methods=[mediaPicker_didPickMediaItems_],protocols=['mediaPickerDelegate'])
mpDelegate = mediaPickerDelegate.alloc().init()

def pick_music():
	mp1 = MPicker.alloc().initWithMediaTypes_(1)
	mp1.setDelegate_(mpDelegate)
	mp1.allowsPickingMultipleItems = False
	
v = ui.load_view('myui')
v.present('sheet')
# --------------------
#!python2

from objc_util import *
import ui

MPicker = ObjCClass('MPMediaPickerController')

def mediaPicker_didPickMediaItems_(_self, _cmd, _mp, _collection):
	picker = ObjCInstance(_mp)
	print('!!!', picker, ObjCInstance(_collection))
	picker.dismissViewControllerAnimated_completion_(True, None)
	
def mediaPickerDidCancel_(_self, _cmd, _mp):
	ObjCInstance(_mp).dismissViewControllerAnimated_completion_(True, None)
	
MediaPickerDelegate = create_objc_class('MediaPickerDelegate', methods=[mediaPicker_didPickMediaItems_, mediaPickerDidCancel_], protocols=['MPMediaPickerDelegate'])
mpDelegate = MediaPickerDelegate.alloc().init()

# Set "pick_music" as the action of a button in "myui.pyui"
def pick_music(sender):
	mp1 = MPicker.alloc().initWithMediaTypes_(1)
	mp1.setDelegate_(mpDelegate)
	mp1.allowsPickingMultipleItems = False
	root_vc = UIApplication.sharedApplication().keyWindow().rootViewController()
	while root_vc.presentedViewController():
		root_vc = root_vc.presentedViewController()
	root_vc.presentViewController_animated_completion_(mp1, True, None)
	
v = ui.load_view('myui')
v.present('sheet')
# --------------------
#Pythonista Forum - @Phuket2
import ui, editor

def pyui_bindings(obj):
	# Pythonista Forum, @JonB
	def WrapInstance(obj):
		class Wrapper(obj.__class__):
			def __new__(cls):
				return obj
		return Wrapper
		
	bindings = globals().copy()
	bindings[obj.__class__.__name__] = WrapInstance(obj)
	return bindings
	
# a Custom ui class as it subclasses ui.View
class MYUIClass(ui.View):
	def __init__(self, ui_file, *args, **kwargs):
		ui.load_view(ui_file, pyui_bindings(self))
		super().__init__(*args, **kwargs)
		ui.View.__init__(self, *args, **kwargs)
		
	# this is a callback from ui, is called automatically for a custom
	# class, if the method is defined
	def will_close(self):
		print('the view will close')
		
	def did_load(self):
		print('the pyui file has loaded...')
		
if __name__ == '__main__':
	_use_theme = True
	w, h = 320, 320
	f = (0, 0, w, h)
	
	ui_file = 'myui'
	style = 'sheet'
	animated = False
	theme = 'Oceanic'
	hide_title_bar = False
	
	mc = MYUIClass(ui_file, frame=f, bg_color='white')
	
	if not _use_theme:
		mc.present('sheet', animated=animated,
		hide_title_bar=hide_title_bar)
	else:
		mc.name = theme
		editor.present_themed(mc, theme_name=theme,
		style=style, animated=animated,
		hide_title_bar=hide_title_bar)
# --------------------

