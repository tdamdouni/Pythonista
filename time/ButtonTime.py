# http://omz-forums.appspot.com/pythonista/post/5892460416860160
# coding: utf-8
import ui
import time
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
		
def some_function():
	## do stuff here...
	ui.delay(some_function, .5) ## half-second delay
	
def button_pressed(sender):
	## do whatever...
	ui.delay(some_function, .5) ## half-second delay
	
## don't forget to cancel your delays...
ui.cancel_delays()

