# coding: utf-8

# https://forum.omz-software.com/topic/3007/updating-a-webview

import ui
import tempfile
import os
import console

def ButtonClick(sender):
	v1 = sender.superview
	#w=v1['webview1']
	#console.alert(str(w))
	w.load_html('<!DOCTYPE html><html><body><h1>My Second Heading</h1></html>')
	#w.present()
	
v = ui.load_view('Test')

w=v['webview1']
w.load_html('<!DOCTYPE html><html><body><h1>My First Heading</h1></html>')

v.present('fullscreen')

