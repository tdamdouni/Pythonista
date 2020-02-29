#!python2
# coding: utf-8

# https://forum.omz-software.com/topic/2847/2-easy-questions/8

from __future__ import print_function
import ui

def btn_action(sender):
	# sender is the button
	
	# could do the below line, maybe not so clear... so will write it out
	#the_value = int(sender.connected_label.text)
	lb = sender.connected_label # dynamically created attribute
	int_val = int(lb.text)
	the_value = int_val
	print(the_value)
	lb.text = str(the_value + sender.increment_value)
	
	
	
f = (0,0,200,200)
v = ui.View(frame = f)
v.bg_color = 'white'
lb = ui.Label(frame = (10,10,100, 32))
lb.text = '1001'
btn = ui.Button(frame = (10, lb.height + 30, 80, 32))
btn.title = 'Hit Me'
btn.action = btn_action
btn.border_width = .5
btn.corner_radius = 3
'''
    very important, the 2 next lines of code are referencing attributes that dont exist in a ui.Button. They are created dynamically because you assign a value to them ( i think thats the right jargon)
'''
btn.connected_label = lb
btn.increment_value = 10

v.add_subview(btn)
v.add_subview(lb)
v.present('sheet')

