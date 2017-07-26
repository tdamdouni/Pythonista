# https://forum.omz-software.com/topic/3602/basic-doubt-with-linking-segmented-control

# Just To Update The TextField With Choice
# Made In Segmented control

# coding: utf-8

import ui

def segment_action(sender):
	if control.selected_index == 0:
		sender.superview['text_field'].text = 'Hello'
	elif control.selected_index == 1:
		sender.superview['text_field'].text ='World'

view = ui.View()
view.name = 'Segment'
view.frame = (0,0,360,600)
view.bg_color='white'

text_field = ui.TextField()
text_field.frame = (130,200,100,50)
#text_field.text = 'Namaste'
text_field.name = 'text_field'
text_field.alignment = 1
view.add_subview(text_field)

control = ui.SegmentedControl()
control.frame =(130,50,100,50)
control.segments = ('q' , 'q')

control.action = segment_action

view.add_subview(control)

view.present('sheet')
