# https://forum.omz-software.com/topic/3609/gui-textfield-example/5

import ui

user_value = '120'
def text_entered(sender):
	user_value = sender.text
	print(user_value)
	
text_field = ui.TextField()
text_field.action = text_entered
text_field.text = user_value
text_field.present()

