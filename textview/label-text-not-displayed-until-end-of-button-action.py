# https://forum.omz-software.com/topic/3495/label-text-not-displayed-until-end-of-button-action/5

import ui

@ui.in_background
def myaction(sender):
	sender.text = "Hello!"
	time.sleep(2)
	sender.text = "Bye!"
	
ui.load_view().present()

# --------------------

import ui
from functools import partial

def delay_action(sender):
	sender.title = 'bye'
	
def button_tapped(sender):
	sender.title = 'Hello'
	ui.delay(partial(delay_action, sender), 3)
	
view = ui.View(frame=(0,0,200,200))                                     # [1]
view.name = 'Demo'                                    # [2]
view.background_color = 'white'                       # [3]
button = ui.Button(title='Tap me!')                   # [4]
button.center = (view.width * 0.5, view.height * 0.5) # [5]
button.flex = 'LRTB'                                  # [6]
button.action = button_tapped                         # [7]
view.add_subview(button)                              # [8]
view.present('sheet')                                 # [9]

# --------------------

def run_async(func):
	from threading import Thread
	from functools import wraps
	
	@wraps(func)
	def async_func(*args, **kwargs):
		func_hl = Thread(target = func, args = args, kwargs = kwargs)
		func_hl.start()
		return func_hl
		
	return async_func
# --------------------
@run_async
def myaction(sender):
	your code here

