from __future__ import print_function
# Jan 2, 2016, 10:12 AM
# Tutorial Doctor

# https://forum.omz-software.com/topic/2524/codeshare-animated-view

# https://github.com/TutorialDoctor/Pythonista-Projects

# Add a ui to this file and add a custom view named view2. Add your controls to view2 and run the script. 
# view 2 should animate in when you press the +, and animate out when you press the greater than sign.
# Additionaly, some toolbar options should be added to the main view.

import ui,sound
print(ui)
# Action Functions
#--------------------------------------------------------------------	
def move_left(sender):
	def left():
		view2.x=0
		#view2 is a custom view located to the right of the main view
		# add suviews to this view if you please.
		r[0].action=move_right
	r[0].title='>'
	ui.animate(left,.5)


def move_right(sender):
	def right():
		r[0].action=move_left
		view2.x = window.width
	r[0].title='+'
	ui.animate(right,.5)


def close(sender):
	window.close()
def check(sender):
	sound.play_effect('Woosh_1')
def error(sender):
	sound.play_effect('Error')
def clip(sender):
	sound.play_effect('Clock_1')
#--------------------------------------------------------------------	


# Setup
#--------------------------------------------------------------------	
window = ui.load_view()
view2=window['view2']
view2.x = window.width
view2.height = window.height
view2.width = window.width
#--------------------------------------------------------------------	


# Functions
#--------------------------------------------------------------------	
def create_l_buttonItems(*buttons):
	items=[]
	for b in buttons:
		b=ui.ButtonItem(b)
		b.tint_color='white'
		items.append(b)
	return items


def create_r_buttonItems(*buttons):
	items=[]
	for b in buttons:
		b=ui.ButtonItem(b)
		b.tint_color='white'
		b.action=move_left
		if b.title=='>':
			b.action=move_right
		items.append(b)
	return items
#--------------------------------------------------------------------	


# Implementation
#--------------------------------------------------------------------	
l = create_l_buttonItems('File','|','Edit','|','About')
window.left_button_items = l
r = create_r_buttonItems('+')
window.right_button_items = r
l[1].enabled=False 
l[3].enabled=False 
window.present('fullscreen',title_bar_color='#635D51')


#--------------------------------------------------------------------	


# Testing
#--------------------------------------------------------------------	
for item in l:
	print(item.title)
for item in r:
	print(item.title)
#--------------------------------------------------------------------	


# Notes and discoveries
#--------------------------------------------------------------------	
# If you write good functions, the implementation should be short and simple to type and understand. Comments shouldnt be needed in this case.
# This code is still not as refactorable as it can be.
#--------------------------------------------------------------------	