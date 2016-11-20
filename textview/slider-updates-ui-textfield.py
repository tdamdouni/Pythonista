# coding: utf-8

# https://forum.omz-software.com/topic/3051/ui-textfield-drives-slider/7

# I can't find if I can send an image here so I'll try to describe ui in text

# Text.field (displays slider value)

# Slider (updates textfield taking multiplier value from which of three switches is active)

# Switch 1(makes text field display slider in metres)
# Switch 2(displays in feet)
# Switch 3(displays in milliseconds/ speed of sound)

# Label(displays value of active switch and changes text colour to match switch Color)

import ui
import clipboard
import decimal
from random import random
from console import hud_alert

def switch_action1(sender):
	'@type sender: ui.Switch'
	v = sender.superview
	sw1 = v['switch1'].value
	sw2 = v['switch2']
	sw3 = v['switch3']
	if (sw1):
		value = 1
		sw2.value = False
		sw3.value = False
		
def switch_action2(sender):
	'@type sender: ui.Switch'
	v = sender.superview
	sw1 = v['switch1']
	sw2 = v['switch2'].value
	sw3 = v['switch3']
	if (sw2):
		value = 1
		sw1.value = False
		sw3.value = False
		
def switch_action3(sender):
	'@type sender: ui.Switch'
	v = sender.superview
	sw1 = v['switch1']
	sw2 = v['switch2']
	sw3 = v['switch3'].value
	if (sw3):
		value = 1
		sw1.value = False
		sw2.value = False
		
def slider_action(sender):
	v = sender.superview
	numbers = v['slider1'].value
	v['numberval'].text = '%.fm' % (numbers*100.00)
	v['mval'].text = '%.2fm' % (numbers*100.00)
	v['msval'].text = '%.3fms' % (numbers*2.92*100)
	v['ftval'].text = '%.2fft' % (numbers*3.37*100)
	sw1 = v['switch1'].value
	sw2 = v['switch2'].value
	sw3 = v['switch3'].value
	metres = v['mval'].text
	msecs = v['msval'].text
	feet = v['ftval'].text
	if sw1:
		value = 1
		v['mfield'].text = metres
		v['numberval'].text = metres
		v['numberval'].text_color = 'd25050'
		v['slider1'].tint_color = 'd25050'
	if sw2:
		value = 1
		v['mfield'].text = msecs
		v['numberval'].text = msecs
		v['numberval'].text_color = '6bc68b'
		v['slider1'].tint_color = '6bc68b'
	if sw3:
		value = 1
		v['mfield'].text = feet
		v['numberval'].text = feet
		v['numberval'].text_color = '6a93fb'
		v['slider1'].tint_color = '6a93fb'
		
v = ui.load_view('VertecAxUi')
slider_action(v['slider1'])
switch_action1(v['switch1'])
switch_action2(v['switch2'])
switch_action3(v['switch3'])

if ui.get_screen_size()[1] >= 768:
	v.present('popover')
else:
	v.present()

