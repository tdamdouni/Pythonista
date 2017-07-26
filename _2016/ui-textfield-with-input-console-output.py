# https://forum.omz-software.com/topic/3698/how-to-save-user-input-from-text-field-and-use-throughout-script-with-ui/8

import ui
v=ui.View(frame=(0,0,500,500))
t=ui.TextField(frame=(0,0,300,75))
v.add_subview(t)
def tfaction(textfield):
	'''when you change the textfield, and press return, this metjod is called'''
	print('textfield changed:', textfield.text )
t.action=tfaction
v.present('sheet')

