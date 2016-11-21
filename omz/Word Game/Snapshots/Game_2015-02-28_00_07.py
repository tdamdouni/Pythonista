# coding: utf-8

import sk
import ui
import sound
import marshal
import string
import math
from itertools import product, chain
from random import choice
from copy import copy

screen_w, screen_h = ui.get_screen_size()
min_screen = min(screen_w, screen_h)

cols = 10
rows = 10
tile_size = min_screen / (max(cols, rows) + 1)
font_size = int(tile_size * 0.7)

# Derived from: http://en.m.wikipedia.org/wiki/Letter_frequency
letter_freq = {'a': 8.2, 'b': 1.5, 'c': 2.8, 'd': 4.3,
'e': 12.7, 'f': 2.3, 'g': 2.0, 'h': 6.1, 'i': 7.0, 'j': 0.2, 
'k': 7.7, 'l': 4.0, 'm': 2.4, 'n': 6.7, 'o': 7.5, 'p': 1.9,
'q': 0.1, 'r': 6.0, 's': 6.3, 't': 9.0, 'u': 2.8, 'v': 1.0,
'w': 2.4, 'x': 0.2, 'y': 2.0, 'z': 0.1}
letter_bag = list(chain(*[[letter] * int(letter_freq[letter]*10) for letter in letter_freq]))

class Game (sk.Scene):
	def __init__(self):
		with open('words_en.data') as f:
			self.words = marshal.load(f)
		self.root = sk.Node()
		self.add_child(self.root)
		self.background_color = '#0b1d28'
		textures = {}
		for letter in letter_freq:
			with ui.ImageContext(tile_size, tile_size) as ctx:
				shadow = ui.Path.rounded_rect(2, 2, tile_size-4, tile_size-4, 5)
				ui.set_color('silver')
				shadow.fill()
				
				bg = ui.Path.rounded_rect(2, 2, tile_size-4, tile_size-8, 5)
				ui.set_color('white')
				bg.fill()
				font = ('AvenirNext-Regular', font_size)
				w, h = ui.measure_string(letter.upper(), font=font)
				x, y = (tile_size - w)/2, (tile_size - h)/2
				ui.draw_string(letter.upper(), rect=(x, y, w, h), font=font, color='black')
				textures[letter] = sk.Texture(ctx.get_image())
		self.tile_textures = textures
		self.tiles = [] #[[None]*rows for i in xrange(cols)]
		for x, y in product(xrange(cols), xrange(rows)):
			s = self.create_tile(x, y)
			self.tiles.append(s)
			self.root.add_child(s)
		self.selected = []
		self.touched_tile = None
		self.score_label = sk.LabelNode()
		self.score_label.font_name = 'AvenirNext-Regular'
		self.score_label.font_size = 50
		self.score_label.h_align = sk.H_ALIGN_CENTER
		self.score_label.text = '0'
		self.score = 0
		self.add_child(self.score_label)
		self.did_change_size(None)
	
	def create_tile(self, x, y):
		letter = choice(letter_bag)
		s = sk.SpriteNode(self.tile_textures[letter])
		s.user_info = {'letter': letter, 'x': x, 'y': y}
		pos_x = tile_size/2 + x*tile_size
		pos_y = tile_size/2 + y*tile_size
		if x % 2 != 0:
			pos_y += tile_size/2
		s.position = pos_x, pos_y
		s.color_blend_factor = 1
		s.color = 'white'
		return s
		
	def did_change_size(self, old_size):
		x_margin = (self.size[0] - cols * tile_size)/2
		y_margin = (self.size[1] - rows * tile_size)/2 - tile_size/2
		self.root.position = x_margin, y_margin
		if self.size[0] < self.size[1]:
			self.score_label.position = self.size[0]/2, self.size[1] - 100
			self.score_label.font_size = 60
		else:
			self.score_label.position = x_margin/2, self.size[1] - 100
			self.score_label.font_size = 40
	
	def get_selected_word(self):
		return ''.join([t.user_info['letter'] for t in self.selected]).lower()
	
	def touch_to_tile(self, location):
		touch_x = location[0] - self.root.position[0]
		touch_y = location[1] - self.root.position[1]
		x = int(touch_x / tile_size)
		if x % 2 != 0:
			y = int((touch_y - tile_size/2) / tile_size)
		else:
			y = int(touch_y / tile_size)
		return x, y
	
	def tile_at(self, location):
		x = location[0] - self.root.position[0]
		y = location[1] - self.root.position[1]
		for tile in self.tiles:
			if sk.point_distance((x, y), tile.position) < tile_size/2:
				if tile.alpha < 1:
					continue
				return tile
		return None
	
	def is_neighbor(self, tile1, tile2):
		if (not tile1 or not tile2 or tile1 == tile2):
			return True
		x1, y1 = tile1.user_info['x'], tile1.user_info['y']
		x2, y2 = tile2.user_info['x'], tile2.user_info['y']
		if x1 == x2:
			return abs(y2-y1) <= 1
		elif x1 % 2 == 0:
			return abs(x2-x1) <= 1 and -1 <= (y2-y1) <= 0
		else:
			return abs(x2-x1) <= 1 and 0 <= (y2-y1) <= 1
	
	def select_tile(self, tile):
		if not tile or (self.selected and self.selected[-1] == tile):
			return
		if tile in self.selected:
			self.selected = self.selected[:self.selected.index(tile)+1]
		else:
			if self.selected:
				last_selected = self.selected[-1]
				if not self.is_neighbor(tile, last_selected):
					self.selected = []
				self.selected.append(tile)
			else:
				self.selected = [tile]
		for tile in self.tiles:
			tile.color = '#fdffce' if tile in self.selected else 'white'
		sound.play_effect('UI/click1')
		
	
	def calc_score(self, word_tiles):
		n = len(word_tiles)
		return (n * (n + 1)) * 10
	
	def submit_word(self):
		word = self.get_selected_word()
		if not word:
			return
		if word + '\n' in self.words:
			sound.play_effect('Digital/PowerUp7')
			self.score += self.calc_score(self.selected)
			self.score_label.text = str(self.score)
		else:
			sound.play_effect('Digital/PhaserDown3')
			for tile in self.selected:
				tile.color = 'white'
			self.selected = []
			self.touched_tile = None
		for tile in self.selected:
			tile.run_action(sk.Action.fade_out(0.25))
			tile.run_action(sk.Action.scale_to(0.5, 0.25))
		self.tiles[:] = [t for t in self.tiles if t not in self.selected]
		sorted_selection = sorted(self.selected, key=lambda t: t.user_info['y'], reverse=True)
		new_tiles_by_col = [0] * cols
		offsets = [0] * len(self.tiles)
		for t in sorted_selection:
			x, y = t.user_info['x'], t.user_info['y']
			new_tiles_by_col[x] += 1
			for i, tile in enumerate(self.tiles):
				if tile.user_info['x'] == x and tile.user_info['y'] > y:
					tile.user_info['y'] -= 1
					offsets[i] += 1
		for i, offset in enumerate(offsets):
			if offset > 0:
				tile = self.tiles[i]
				d = 0.15 * offset
				move = sk.Action.move_by(0, -offset * tile_size, d)
				move.timing_mode = sk.TIMING_EASE_IN
				tile.run_action(move)
		for i, n in enumerate(new_tiles_by_col):
			for j in xrange(n):
				s = self.create_tile(i, rows-j-1)
				to_pos = s.position
				from_pos = to_pos[0], (rows + n-j) * tile_size
				s.position = from_pos
				self.tiles.append(s)
				self.root.add_child(s)
				s.alpha = 0
				s.run_action(sk.Action.fade_in(0.25))
				move = sk.Action.move_to(*to_pos)
				move.duration = (from_pos[1] - to_pos[1]) / tile_size * 0.15
				move.timing_mode = sk.TIMING_EASE_IN
				s.run_action(move)
		self.selected = []
		self.touched_tile = None
	
	def touch_began(self, touch):
		last_touched_tile = self.touched_tile
		self.touched_tile = self.tile_at(touch.location)
		if last_touched_tile == self.touched_tile:
			self.submit_word()
		elif self.touched_tile:
			self.select_tile(self.touched_tile)
	
	def touch_moved(self, touch):
		self.select_tile(self.tile_at(touch.location))
	
	def touch_ended(self, touch):
		tile = self.tile_at(touch.location)
		if tile == self.touched_tile:
			self.select_tile(tile)
		else:
			self.submit_word()

def main():
	game = Game()
	scene_view = sk.View()
	scene_view.run(game)
	scene_view.present()

if __name__ == '__main__':
	main()