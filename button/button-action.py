# https://forum.omz-software.com/topic/3495/label-text-not-displayed-until-end-of-button-action/9

import time, ui

@ui.in_background
def myaction(sender):
	sender.superview["Record_label"].text = "START" # write to the label
	time.sleep(2) # delay for a bit
	sender.superview["Record_label"].text = "END" # write to the label
	
def make_button(title='Click me'):
	button = ui.Button(name=title, title=title)
	button.action = myaction
	return button
	
def make_label(text='Who cuts your hair?'):
	label = ui.Label(name='Record_label', frame=(50, 50, 200, 32))
	label.text = text
	label.text_color = 'blue'
	return label
	
if __name__ == '__main__':
	view = ui.View()
	view.add_subview(make_button())
	view.add_subview(make_label())
	view.present()
	view['Click me'].center = view.center

