# coding: utf-8

# https://forum.omz-software.com/topic/1134/change-the-text-of-a-label-in-the-ui

import ui
import console

v = ui.load_view('myUI')
v.present('sheet')

def entername():
	mytext = console.input_alert('Please enter text:')
	textlabel = v['textlabel']
	textlabel.text = mytext
	
entername()

