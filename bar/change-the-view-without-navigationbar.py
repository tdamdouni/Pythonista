# coding: utf-8

# https://forum.omz-software.com/topic/2854/change-the-view-without-navigationbar

import ui

def button_action(sender):
	sender.superview.hidden = True
	sender.v2.present('sheet', animated = False)
	
f = (0,0,500,500)
v1 = ui.View(frame = f, bg_color = 'white')
btn = ui.Button(frame = (10,10,150,32), title = 'hit me')
btn.border_width = .5
btn.corner_radius = 3
btn.action = button_action
v1.add_subview(btn)

v2 = ui.View(frame = f)
v2.bg_color = 'pink'

btn.v2 = v2   # not a attr of ui.Button, is being dynamically created
v1.present('sheet')

# --------------------

import ui

container = ui.View()
a=ui.load_view('intro.pyui')
b=ui.load_view('mail.pyui')

def switch_to_mail():
	container.remove_subview(a)
	container.add_subview(b)
	
container.add_subview(a)
container.present(hide_title_bar=1)
ui.delay(switch_to_mail,1)

# --------------------

def openMail(sender):
	global View
	View.close()
	View.wait_modal() #VERY IMPORTANT, waits for view to close completely
	View = ui.loadview('mail.pyui')
	View.present('sheet')
	
View = ui.loadview('intro.pyui')
mail_button = ui.ButtonItem(action=openMail, title = 'Open Mail')
View.right_button_items =[mail_button]
View.present('sheet')

# --------------------

