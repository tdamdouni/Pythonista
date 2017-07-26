# Simple demo of playing a looping sound using the (currently undocumented) sound.Player class

# https://gist.github.com/omz/10023837

# https://forum.omz-software.com/topic/611/how-to-repeat-sound/2

# In case anybody else is dredging the forums trying to figure out how the sound module works, sound.play_effect() actually takes up to 5 parameters. The last one makes it repeat:

# effect = sound.play_effect('my_sound.wav', volume, pitch, unknown, repeat)

# If repeat is anything that evaluates to True, the sound seems to repeat until you call sound.stop_effect(effect). I have no idea what the unknown parameter does.

import sound
import os
from scene import *

class MyScene (Scene):
	def setup(self):
		self.player = sound.Player(os.path.expanduser('~/Pythonista.app/Beep.caf'))
		self.player.number_of_loops = -1 #repeat forever
		self.playing = False
	
	def draw(self):
		background(0, 0, 0)
		x, y = self.size.w * 0.5, self.size.h * 0.5
		text('Touch to play/pause', 'Helvetica', 30, x, y)
	
	def touch_began(self, touch):
		if self.playing:
			self.player.stop()
		else:
			self.player.play()
		self.playing = not self.playing
			
run(MyScene())

