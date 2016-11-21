# http://stackoverflow.com/questions/28146930/i-cannot-get-the-restart-button-to-work-on-my-stopwatch-using-pythonista-on-iph

import ui
from time import *
start = int(time())
def stop_time(sender):
	finish = int(time())
	total_time = int(finish - start)
	button1 = str("Your time is %i seconds." % (total_time))
	sender.title = None
	sender.title = str(button1)

def restart_time(sender):
	start = int(time())
	button2 = str("Stopwatch restarted.")
	sender.title = None
	sender.title = str(button2)
ui.load_view('stop_time').present('sheet')

def restart_time(sender):
	global start
	start = int(time())
	button2 = str("Stopwatch restarted.")
	sender.title = None
	sender.title = str(button2)

