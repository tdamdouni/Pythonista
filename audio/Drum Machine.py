#TODO: Adjust size to screen size (iPhone)
#TODO: Clear (and random, play/pause?) buttons

from scene import *
from sound import play_effect, set_volume, load_effect
from colorsys import hsv_to_rgb
import pickle

class DrumMachine (Scene):
	def setup(self):
		self.beat = 0.0
		set_volume(1.0)
		
		self.sounds = ['Drums_01', 'Drums_02', 'Drums_03', 'Drums_06',
		'Drums_10', 'Drums_11', 'Drums_11', 'Drums_15']
		for effect in self.sounds:
			load_effect(effect)
			
		try:
			with open('Drums.data', 'r') as f:
				self.grid = pickle.load(f)
		except EOFError:
			self.grid = [[False for col in xrange(16)] for row in xrange(8)]
			
	def draw(self):
		background(0, 0, 0)
		last_beat = int(self.beat)
		self.beat += 1.0/7.5
		self.beat %= 16
		play = int(self.beat) != last_beat
		for y in xrange(16):
			beat_row = int(self.beat) == y
			for x in xrange(8):
				if self.grid[x][y]:
					h = x / 8.0
					r, g, b = hsv_to_rgb(h, 1, 1)
					if play and int(self.beat) == y:
						play_effect(self.sounds[x])
					if beat_row:
						h = x / 8.0
						r, g, b = hsv_to_rgb(h, 1, 1)
						fill(r, g, b)
					else:
						r, g, b = hsv_to_rgb(h, 1, 0.5)
						fill(r, g, b)
				elif beat_row:
					fill(1, 1, 1)
				else:
					fill(0.50, 0.50, 0.50)
				rect(x * 96, y * 61, 95, 60)
				
	def touch_began(self, touch):
		x, y = touch.location.as_tuple()
		x = int(x / 96)
		y = int(y / 61)
		if y < 16:
			self.grid[x][y] = not self.grid[x][y]
			
	def stop(self):
		with open('Drums.data', 'w') as f:
			pickle.dump(self.grid, f)
			
run(DrumMachine(), PORTRAIT)

