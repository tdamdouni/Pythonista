# https://forum.omz-software.com/topic/4219/how-to-break-out-of-loop-using-ui-button/5

import ui
import time
#running= True
def button_tapped(sender):
	'@type sender: ui.Button'
	print('Done!')
	sender.enabled = False          # setting the enabled attr to false
	#running = False
	#ui.close_all()
	
# broken this call into 2 parts. i am not sure the reasin, but if you need the a a reference
# to the view back, it has some problems.
v = ui.load_view('done_button')
v.present('sheet')

while True:
	#if running == False: commented out
	# here, we are looking at the uiButton.enabled attr to decide if its been clicked
	# your script was also not working correctly if you closed your window.
	# so we are checking the ui.Views attr on_screen. if the view is closed v.on_screen
	# would be False so we should also break out f the while loop.
	if not v['button1'].enabled or not v.on_screen:
		print('out of here')
		break
	print('running')
	time.sleep(2)

