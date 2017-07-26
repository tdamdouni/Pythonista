# https://forum.omz-software.com/topic/4025/one-function-for-all-ui-buttons/6

import ui

def create_btn(id, *args, **kwargs):
	btn = ui.Button(**kwargs)   # ---> passes the kwargs to the Button __init__ (2.7 or 3.5)
	btn.id = id                 # ---> adds the attribute id to ui.Button
	return btn
	
def button_action(sender):
	# using this func for all buttons. Could use the id to determine what to do for which btn
	print(sender.id, sender.title)
	
if __name__ == '__main__':
	v = ui.View(frame=(0, 0, 200, 300), bg_color='white')
	btn1 = create_btn(1, title='OK', border_width=.1, frame=(50, 50, 50, 100),
	action=button_action, bg_color='red', tint_color='white', corner_radius = 3)
	btn1.width=100    # the width is not set by the frame kwargs, i think because,
																		# size_to_fit is automatically called when the button is created
																		# i cant remember, maybe theres a way to override that so you dont need
																		# the extra call to set the width
																		
	btn2 = create_btn(2, title='Cancel', border_width=1, frame=(50, 90, 100, 200),
	action=button_action, bg_color='green', tint_color='white', corner_radius = 3)
	btn2.width=100
	
	v.add_subview(btn1)
	v.add_subview(btn2)
	v.present('sheet')

