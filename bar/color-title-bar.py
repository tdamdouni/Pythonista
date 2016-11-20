# https://forum.omz-software.com/topic/3657/how-do-i-change-color-of-top-bar/3

import time, ui

class Interface():

	@ui.in_background
	def Switch(sender):
		if Interface.bgcolour == 'red':
			Interface.bgcolour = 'blue'
			Interface.btn.title = 'Red!'
		else:
			Interface.bgcolour = 'red'
			Interface.btn.title = 'Blue!'
		Interface.v.close()
		time.sleep(1)
		Interface.v.background_color = Interface.bgcolour
		Interface.v.present('sheet', title_bar_color = Interface.bgcolour)
		
	btn = ui.Button()
	btn.title = 'Blue!'
	btn.x = 0
	btn.y = 0
	btn.width = 300
	btn.height = 300
	btn.action = Switch
	
	bgcolour = 'red'
	v = ui.View(background_color = bgcolour)
	v.add_subview(btn)
	v.width = 300
	v.height = 300
	
x = Interface()
x.v.present('sheet', title_bar_color = 'red')

