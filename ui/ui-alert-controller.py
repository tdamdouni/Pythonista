#!python2
# coding: utf-8

# https://forum.omz-software.com/topic/2314/share-code-uialertcontroller/2

# https://forum.omz-software.com/topic/2670/how-can-i-present-a-uialertcontroller/4

from __future__ import print_function
from objc_util import *
import ctypes
import ui

SUIViewController = ObjCClass('SUIViewController')
UIAlertController = ObjCClass('UIAlertController')
UIAlertAction     = ObjCClass('UIAlertAction')

def ok_pressed(sender):
	print('OK pressed')
	
alert = UIAlertController.alertControllerWithTitle_message_preferredStyle_(ns('My Alert'), ns('My Message'), 1)
alert_action_block = ObjCBlock(ok_pressed, None, [c_void_p])
default_action = UIAlertAction.actionWithTitle_style_handler_(ns('OK'), 0, None)
alert.addAction_(default_action)
##rvc.presentModalViewController_animated_(alert, True)

## Stop Crashes
retain_global(alert_action_block)

def button_tapped(sender):
	super_view = sender.superview
	super_view_pntr = ObjCInstance(super_view)
	vc = SUIViewController.viewControllerForView_(super_view_pntr)
	vc.presentModalViewController_animated_(alert, True)
	
view = ui.View(frame=(0,0,500,500))
view.name = 'Demo'
view.background_color = 'white'
button = ui.Button(title='Tap me!')
button.center = (view.width * 0.5, view.height * 0.5)
button.flex = 'LRTB'
button.action = button_tapped
view.add_subview(button)
view.present('sheet')

