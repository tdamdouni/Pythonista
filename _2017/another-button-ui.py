# https://forum.omz-software.com/topic/4025/one-function-for-all-ui-buttons/10

import ui

w, h = ui.get_screen_size()
bw = 100
bh = 50


def button_tapped(sender):
	label.bg_color = sender.bg_color
	label.text = sender.title
	label.text_color = sender.tint_color
	print(label.bg_color)
	
	
def make_button(title, screen_x, super_view):
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
	super_view.add_subview(button)
	return button
	
	
label = ui.Label(
    alignment=ui.ALIGN_CENTER,
    bg_color='silver',
    border_color='black',
    border_width=1,
    frame=(300, 100, 200, 100),
    name='Label')

view = ui.View(name='Color fun', bg_color='darkgrey', frame=(0, 0, w, h))
view.add_subview(label)
buttons = {color: make_button(title=color, screen_x=200 + 100 * i,
                              super_view=view)
           for i, color in enumerate(['blue', 'red', 'yellow', 'green'])}
buttons['yellow'].tint_color = 'black'
view.present('screen')

