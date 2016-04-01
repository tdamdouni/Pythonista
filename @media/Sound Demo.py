# https://gist.github.com/omz/10023837
# Simple demo of playing a looping sound using the (currently undocumented) sound.Player class

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