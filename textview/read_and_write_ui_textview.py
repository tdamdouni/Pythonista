# https://gist.github.com/cclauss/5997f9c653c0c4bf1521

import ui

filename = 'name.txt'

def read_username(filename=filename):
	username = None
	try:
		with open(filename) as in_file:
			for line in in_file.readlines():
				username = line.strip() or username
	except IOError:
		pass
	return username or 'Player 1'
	
def write_username(sender, filename=filename):
	username = sender.superview['namefield'].text.strip()  # or 'Player 1'
	if username:
		with open(filename, 'w') as out_file:
			out_file.write(username)
			
def get_username():
	textfield = ui.TextView(name='namefield')
	textfield.text = read_username()
	
	button = ui.Button(title='Save name')
	button.action = write_username
	
	root_view = ui.View(name='get_username()')
	root_view.add_subview(textfield)
	root_view.add_subview(button)
	root_view.hidden = True
	root_view.present('sheet')
	
	textfield.center = button.center = root_view.center
	textfield.height = 25
	root_view.hidden = False
	return root_view
	
root_view = get_username()
root_view.wait_modal()
username = root_view['namefield'].text
print(username)

