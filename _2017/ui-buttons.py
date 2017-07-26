# https://forum.omz-software.com/topic/4025/one-function-for-all-ui-buttons

import ui
def button_tapped(sender):
	lb1.background_color = 'blue'
	lb1.text = 'Blue'
	
def button2_tapped(sender2):
	lb1.background_color = 'red'
	lb1.text = 'Red'
	
def button3_tapped(sender3):
	lb1.background_color = 'yellow'
	lb1.text = 'Yellow'
	
def button4_tapped(sender4):
	lb1.background_color = 'green'
	lb1.text = 'Green'
	
w,h = ui.get_screen_size()
bh = 50
bw = 100
mg = 5
view = ui.View(name = 'Color fun', bg_color = 'darkgrey', frame = (0,0,w,h))
view.present('screen')

lb1 = ui.Label(name = 'Label1', bg_color = 'silver')
lb1.frame = (300,100,200,100)
lb1.border_color = 'black'
lb1.border_width = 1
lb1.alignment = ui.ALIGN_CENTER

button = ui.Button(title = 'Blue', alignment=ui.ALIGN_CENTER, bg_color = 'white', font_color = 'black')
button.frame = (200,900,100,50)
button.tint_color = 'black'
button.border_width = 1
button.action =button_tapped

button2 = ui.Button(title = 'Red', alignment=ui.ALIGN_CENTER, bg_color = 'white')
button2.frame = (300,900,100,50)
button2.tint_color = 'black'
button2.border_width = 1
button2.action = button2_tapped

button3 = ui.Button(title = 'Yellow', alignment=ui.ALIGN_CENTER, bg_color =  'white')
button3.frame = (400,900,100,50)
button3.tint_color = 'black'
button3.border_width = 1
button3.action = button3_tapped

button4 = ui.Button(title = 'Green', alignment=ui.ALIGN_CENTER, bg_color = 'white')
button4.frame = (500,900,100,50)
button4.tint_color = 'black'
button4.border_width = 1
button4.action = button4_tapped

view.add_subview(button)
view.add_subview(lb1)
view.add_subview(button2)
view.add_subview(button3)
view.add_subview(button4)

# I would like it something like:
#def button_tapped(sender):
#	if sender == 1:
#		return lb1.bg_color = 'blue'
#	if sender == 2:
#		return lb1.background_color = 'red'
#	if sender == 3:
#		return lb1.backgground_color = 'green'
#	if sender == 4:
#		lb1.background_color = 'yellow'
		
def button_tapped(sender):  # sender is the button itself so you can directly access it's title
	lb1.background_color = sender.title.lower()
	lb1.text = sender.title.title()

