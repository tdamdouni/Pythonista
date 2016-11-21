# https://forum.omz-software.com/topic/1752/using-a-menu-button-as-a-clock-by-constantly-updating-the-button-title

import ui

@ui.in_background
def time_btn(self):
	#self.menu_button(...) just adding a button to
	#aView.right_button_items, returning the button.
		
	btn = self.menu_button('Time', False,None)
	#btn.enabled = False
	while(True):
		if not self.view.on_screen: break
		btn.title = time.strftime('%H:%M:%S')
		time.sleep(1)
			
# --------------------

def some_function():
	## do stuff here...
	ui.delay(some_function, .5) ## half-second delay
	
def button_pressed(sender):
	## do whatever...
	ui.delay(some_function, .5) ## half-second delay
	
## don't forget to cancel your delays...
ui.cancel_delays()


