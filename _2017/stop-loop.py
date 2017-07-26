# https://forum.omz-software.com/topic/4219/how-to-break-out-of-loop-using-ui-button

import ui
import time
running= True
def button_tapped(sender):
	'@type sender: ui.Button'
	print('Done!')
	running = False
	#ui.close_all()
	
ui.load_view('done_button').present('sheet')
while True:
	if running == False:
		print('out of here')
		break
	print('running')
	time.sleep(2)

