# coding: utf-8

# https://forum.omz-software.com/topic/3211/console-output-code/10

from __future__ import print_function
import ui
from objc_util import *
import console
import os
import sys, traceback

NSFileManager = ObjCClass('NSFileManager')

UIDevice = ObjCClass('UIDevice')

print('Enter directory')

path = raw_input()

files = NSFileManager.defaultManager().contentsOfDirectoryAtPath_error_(path,None)
print(files)


@ui.in_background
def file_browser(message):
	alert_result=console.alert(path,path,'Dismiss',hide_cancel_button=True)
	
def back_console(sender):

	console.show_input()
	
@ui.in_background
def about(message):

	alert_result=console.alert('About', 'Project based off of Billy Ellis app called "iFiles" I take no credits for idea of this')
	
def find_ios(sender):

	vers = UIDevice.currentDevice().systemVersion()
	
	string = str(vers)
	
	v = sender.superview
	label = v['label1'].text = string
	
v = ui.load_view()
v.present('sheet')
# --------------------

