# coding: utf-8

# https://forum.omz-software.com/topic/3107/two-instances-of-labels-updated-by-time

#using ui module

import ui
from time import time,sleep,strftime,localtime,gmtime

#t = time()

def reset_action(sender):
	v = sender.superview
'@type sender: ui.Button'
global t
t = time()
start_time = 0.0
stop_time = 0.0

@ui.in_background
def update_time():
	while True:
		#sleep(1)
		ui.delay(0.1)
v['countdown_timer'].text = strftime('%M:%S', gmtime(time()-t))
start_time = 0.0
stop_time = 0.0

#ts = time()

def reset_action2(sender):
	v = sender.superview
'@type sender: ui.Button'
global ts
ts = time()
start_time = 0.0
stop_time = 0.0

@ui.in_background
def update_time2():
	while True:
#sleep(1)
		v['countdown_timer2'].text = strftime('%M%S', gmtime(time()-ts))
start_time = 0.0
stop_time = 0.0

v = ui.load_view('Chessclock')
reset_action(v['reset_button'])
reset_action2(v['reset_button2'])
update_time()
update_time2()

v.present(orientations=['portrait'])

