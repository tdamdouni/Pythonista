# coding: utf-8

import ui

view = ui.load_view('segmented-control')

def button_action(sender):
	if button1.selected_index == 0:
		view['text_label'].text = 'Hello'
	elif button1.selected_index == 1:
		view['text_label'].text ='World'

button1 = view['segmentedcontrol1']
button1.action = button_action

view.present('sheet')