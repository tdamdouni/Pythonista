from __future__ import print_function
# https://forum.omz-software.com/topic/2314/share-code-uialertcontroller

# coding: utf-8

from objc_util import *
import ui

UIAlertController = ObjCClass('UIAlertController')
UIAlertAction     = ObjCClass('UIAlertAction')

def ok_pressed(sender):
    print('OK pressed')

app = UIApplication.sharedApplication()
win = app.keyWindow()
rvc = win.rootViewController()
## this was all setup for thealert view

alert = UIAlertController.alertControllerWithTitle_message_preferredStyle_(ns('My Alert'), ns('My Message'), 1)
alert_action_block = ObjCBlock(ok_pressed, None, [c_void_p])
default_action = UIAlertAction.actionWithTitle_style_handler_(ns('OK'), 0, alert_action_block)
alert.addAction_(default_action)
rvc.presentViewController_animated_completion_(alert, True, None)