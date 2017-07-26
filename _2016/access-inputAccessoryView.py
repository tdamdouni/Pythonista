# coding: utf-8

# https://forum.omz-software.com/topic/2288/no-way-to-end-editing/9

from objc_util import *
import ui
'''set up top level view and textfield'''
v=ui.View()
tf=ui.TextField(frame=[0,0,400,30])
v.add_subview(tf)

tfobj=ObjCInstance(tf)

'''set up toolbar'''
keyboardToolbar=ObjCClass('UIToolbar').alloc().init()
keyboardToolbar.sizeToFit()
flexBarButton=ObjCClass('UIBarButtonItem').alloc().initWithBarButtonSystemItem_target_action_(5,None,None)
doneBarButton=ObjCClass('UIBarButtonItem').alloc().initWithBarButtonSystemItem_target_action_(0,tfobj,sel('endEditing:')) 
keyboardToolbar.items = [flexBarButton, doneBarButton]
tfobj.textField().inputAccessoryView= keyboardToolbar

v.present()
