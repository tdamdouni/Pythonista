# coding: utf-8

# https://forum.omz-software.com/topic/2884/sound-stop_effect-stops-the-sound-with-a-hard-noise-since-last-update-of-version-1-6

from scene import *
import sound
import os

global keyid

class Sound (Scene):

	def setup(self):
		sound.load_effect('Piano_F3')
		
def draw(self):
	pass
	
def touch_began(self, touch):
	global keyid
	keyid = sound.play_effect('Piano_F3')
	
def touch_ended(self, touch):
	global keyid
	sound.stop_effect(keyid)
	
run(Sound(), PORTRAIT)

