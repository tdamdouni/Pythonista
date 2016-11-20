# coding: utf-8

# Captured from: _https://forum.omz-software.com/topic/724/quick-tip-using-ios-system-sound-effects_

import os
import sound
import time

for dirpath, dirnames, filenames in os.walk('/System/Library/Audio/UISounds'):
	for f in filenames:
		if f.endswith('.caf'):
			full_path = os.path.join(dirpath, f)
			sound.play_effect(full_path)
			time.sleep(1)
			
###==============================

# http://en.wikipedia.org/wiki/Blue_box
# http://en.wikipedia.org/wiki/Dual-tone_multi-frequency_signaling

# Change the phone number below and then hold your iOS device next
# to an off-the-hook phone and the DTMF tones will make the call.
#
# Phone companies have learned a lot since the days of phreaking so
# you should expect any calls made to appear on your monthly bill.

phone_number_to_dial = '0081787881218'  # '12345#,765#,*'

import os, sound, time

fmt = '/System/Library/Audio/UISounds/dtmf-{}.caf'

def dial_number(in_phone_number = phone_number_to_dial):
	def dial_digit(in_digit):
		if in_digit == ',':  # a comma is a 2 second pause
			time.sleep(2)
		else:
			sound.play_effect(fmt.format(in_digit))
			time.sleep(0.3)  # changes the dial speed
			
	print('Dialing: %s' % in_phone_number)
	in_phone_number = in_phone_number.replace('#', 'pound').replace('*', 'star')
	for digit in in_phone_number:
		dial_digit(digit)
		
dial_number(phone_number_to_dial)

