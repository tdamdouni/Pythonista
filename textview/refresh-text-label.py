# coding: utf-8

# https://forum.omz-software.com/topic/2849/refresh-text-label
# coding: utf-8

# https://forum.omz-software.com/topic/2849/refresh-text-label/3

from __future__ import print_function
import ui
import random
import time

def dieRoll():
	return random.randint(1, 6)
	
def button_tapped(sender):
	v=sender.superview
	def updateLabel():
		v['lblRoll'].text=str(dieRoll())
		print(v['lblRoll'].text)
		
	for n in range(6) :
		updateLabel()
		v.set_needs_display
		time.sleep(1.0)
		ui.delay(updateLabel,0.5*n)
		#also tried
		#ui.delay(updateLabel,1.0)
		
v = ui.load_view('update-label.pyui')

v.present('sheet')

# The ui.delay approach is good, there's just one logic flaw in your code. You should make the delay time depend on the loop variable n, e.g. something like ui.delay(updateLabel, n) (or multiply n with some factor to make it faster/slower).

# The way you've tried it (with the delay being 1 second for every call) results in all 6 updates being made at once (after 1 second), so you don't really see the individual steps. What you actually want is to do the first update after 1 second, the second after 2, etc., so it makes sense to increase the delay for every step of the animation.

