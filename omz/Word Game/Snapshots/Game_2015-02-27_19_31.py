# coding: utf-8

import sk
import ui
import sound
import marshal
import string
from itertools import product, chain
from random import choice
from copy import copy

screen_w, screen_h = ui.get_screen_size()
min_screen = min(screen_w, screen_h)

padding = 3
cols = 10
rows = 12
tile_size = 80
tile_size = min_screen / (max(cols, rows) + 1) - padding
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
		self.did_change_size(None)
		self.add_child(self.root)
		self.background_color = '#0b1d28'
		textures = {}
		for letter in letter_freq:
			with ui.ImageContext(tile_size, tile_size) as ctx:
				shadow = ui.Path.rounded_rect(0, 0, tile_size, tile_size, 5)
				ui.set_color('silver')
				shadow.fill()
				bg = ui.Path.rounded_rect(0, 0, tile_size, tile_size-4, 5)
				ui.set_color('white')
				bg.fill()
				font = ('AvenirNext-Regular', font_size)
				w, h = ui.measure_string(letter.upper(), font=font)
				x, y = (tile_size - w)/2, (tile_size - h)/2
				ui.draw_string(letter.upper(), rect=(x, y, w, h), font=font, color='black')
				textures[letter] = sk.Texture(ctx.get_image())
		self.tile_textures = textures
		
		self.tiles = [[None]*rows for i in xrange(cols)]
		for x, y in product(xrange(cols), xrange(rows)):
			letter = choice(letter_bag)
			s = sk.SpriteNode(self.tile_textures[letter])
			s.user_info = {'letter': letter, 'x': x, 'y': y}
			pos_x = tile_size/2 + x*(tile_size+padding)
			pos_y = tile_size/2 + y*(tile_size+padding)
			if x % 2 != 0:
				pos_y += tile_size/2
			s.position = pos_x, pos_y
			s.color_blend_factor = 1
			s.color = 'white'
			self.tiles[x][y] = s
			self.root.add_child(s)
		self.selected = []
		self.touched_tile = None
	
	def touch_to_tile(self, location):
		touch_x = location[0] - self.root.position[0]
		touch_y = location[1] - self.root.position[1]
		x = int(touch_x / (tile_size+padding))
		if x % 2 != 0:
			y = int((touch_y - tile_size/2) / (tile_size+padding))
		else:
			y = int(touch_y / (tile_size+padding))
		return x, y
	
	def tile_at(self, location):
		x = location[0] - self.root.position[0]
		y = location[1] - self.root.position[1]
		for tile in chain(*self.tiles):
			if sk.point_distance((x, y), tile.position) < tile_size/2:
				if tile.alpha < 1:
					continue
				return tile
		return None
		
	def did_change_size(self, old_size):
		x_margin = (self.size[0] - cols * (tile_size+padding))/2
		y_margin = (self.size[1] - rows * (tile_size+padding))/2 - tile_size/2
		self.root.position = x_margin, y_margin
	
	def get_selected_word(self):
		return ''.join([t.user_info['letter'] for t in self.selected]).lower()
	
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
		if not tile:
			return
		if self.selected and self.selected[-1] == tile:
			return
		if tile in self.selected:
			self.selected = self.selected[:self.selected.index(tile)+1]
		else:
			if self.selected:
				last_selected = self.selected[-1]
				if self.is_neighbor(tile, last_selected):
					self.selected.append(tile)
				else:
					self.selected = [tile]
			else:
				self.selected = [tile]
		for tile in chain(*self.tiles):
			tile.color = '#fdffce' if tile in self.selected else 'white'
		sound.play_effect('UI/click1')
	
	def submit_word(self):
		word = self.get_selected_word()
		if not word:
			return
		if word + '\n' in self.words:
			sound.play_effect('Digital/PowerUp7')
		else:
			sound.play_effect('Digital/PhaserDown3')
			for tile in self.selected:
				tile.color = 'white'
			self.selected = []
			self.touched_tile = None
		for tile in self.selected:
			tile.run_action(sk.Action.fade_out(0.25))
			tile.run_action(sk.Action.scale_to(0.5, 0.25))
		
		new_tiles = copy(self.tiles)
		for col in self.tiles:
			offset = 0
			for tile in col:
				if tile in self.selected:
					offset += 1
				elif offset > 0:
					#new_tiles[tile.user_info['x']][tile.user_info['y']] = None
					tile.user_info['y'] -= offset
					new_tiles[tile.user_info['x']][tile.user_info['y']] = tile
					tile.run_action(sk.Action.move_by(0, -offset*(tile_size+padding)))
		
		self.selected = []
		self.touched_tile = None
	
	def touch_began(self, touch):
		last_touched_tile = self.touched_tile
		self.touched_tile = self.tile_at(touch.location)
		if last_touched_tile == self.touched_tile:
			self.submit_word()
			return
		if self.touched_tile:
			self.touched_tile.color = '#fdffce'
			self.select_tile(self.touched_tile)
	
	def touch_moved(self, touch):
		if not self.touched_tile:
			return
		tile = self.tile_at(touch.location)
		if tile:
			self.select_tile(tile)
	
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