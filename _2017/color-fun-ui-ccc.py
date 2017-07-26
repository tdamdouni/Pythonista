# https://forum.omz-software.com/topic/4025/one-function-for-all-ui-buttons/2

import ui

w, h = ui.get_screen_size()
bw = 100
bh = 50


def button_tapped(sender):
	label.bg_color = sender.bg_color
	label.text = sender.title
	label.text_color = sender.tint_color
	
	
def make_button(title, screen_x):
	button = ui.Button(
	action=button_tapped,
	alignment=ui.ALIGN_CENTER,
	bg_color=title.lower(),
	border_color='black',
	border_width=1,
	frame=(screen_x, h - 124, bw, bh),
	tint_color='white',
	title=title)
	# it seems to be necessary to reset the frame
	button.frame = (screen_x, h - 124, bw, bh)
	return button
	
	
label = ui.Label(
    alignment=ui.ALIGN_CENTER,
    bg_color='silver',
    border_color='black',
    border_width=1,
    frame=(300, 100, 200, 100),
    name='Label')

button1 = make_button(title='Blue', screen_x=200)
button2 = make_button(title='Red', screen_x=300)
button3 = make_button(title='Yellow', screen_x=400)
button3.tint_color = 'black'  # hard to read white text on a yellow background
button4 = make_button(title='Green', screen_x=500)

view = ui.View(name='Color fun', bg_color='darkgrey', frame=(0, 0, w, h))
view.add_subview(label)
view.add_subview(button1)
view.add_subview(button2)
view.add_subview(button3)
view.add_subview(button4)
view.present('screen')

