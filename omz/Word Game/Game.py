# coding: utf-8

import sk, ui, sound, marshal, string, math, time
from itertools import product, chain
from random import choice, random
from copy import copy
import ui

game_duration = 90
screen_w, screen_h = ui.get_screen_size()
min_screen = min(screen_w, screen_h)
if max(ui.get_screen_size()) >= 768:
	cols, rows = 10, 11
else:
	cols, rows = 7, 7
tile_size = min_screen / (max(cols, rows) + 1)
font_size = int(tile_size * 0.7)

# Derived from http://en.m.wikipedia.org/wiki/Letter_frequency
letter_freq = {'a': 8.2, 'b': 1.5, 'c': 2.8, 'd': 4.3, 'e': 12.7, 'f': 2.3, 'g': 2.0, 'h': 6.1, 'i': 7.0, 'j': 0.2, 'k': 7.7, 'l': 4.0, 'm': 2.4, 'n': 6.7, 'o': 7.5, 'p': 1.9, 'q': 0.1, 'r': 6.0, 's': 6.3, 't': 9.0, 'u': 2.8, 'v': 1.0, 'w': 2.4, 'x': 0.2, 'y': 2.0, 'z': 0.1}
letter_bag = list(chain(*[[letter] * int(letter_freq[letter]*10) for letter in letter_freq]))

with ui.ImageContext(tile_size, tile_size) as ctx:
	ui.set_color('silver')
	ui.Path.rounded_rect(2, 2, tile_size-4, tile_size-4, 4).fill()
	ui.set_color('white')
	ui.Path.rounded_rect(2, 2, tile_size-4, tile_size-6, 4).fill()
	tile_texture = sk.Texture(ctx.get_image())

with ui.ImageContext(100, 100) as ctx:
	ui.set_color('#49b8ff')
	ui.Path.oval(0, 0, 100, 100).fill()
	ui.set_color('white')
	point_bg_tex = sk.Texture(ctx.get_image())

class Tile (sk.SpriteNode):
	def __init__(self, x, y, letter, color='white', multiplier=1):
		sk.SpriteNode.__init__(self, tile_texture)
		self.x = x
		self.y = y
		self.letter = letter
		self._selected = False
		pos_y = y * tile_size + (tile_size/2 if x % 2 == 0 else 0)
		self.position = x * tile_size, pos_y
		self.color_blend_factor = 1
		self.tile_color = color
		self.color = color
		self.label = sk.LabelNode()
		self.label.h_align = sk.H_ALIGN_CENTER
		self.label.v_align = sk.V_ALIGN_CENTER
		self.label.font_name = 'AvenirNext-Regular'
		self.label.font_size = font_size
		self.label.font_color = 'black'
		self.label.text = letter.upper()
		self.multiplier = multiplier
		self.add_child(self.label)
	
	@property
	def selected(self):
		return self._selected
	
	@selected.setter
	def selected(self, value):
		self._selected = value
		self.color = '#fdffce' if value else self.tile_color

class Game (sk.Scene):
	def __init__(self):
		with open('words_en.data') as f:
			self.words = marshal.load(f)
		self.root = sk.Node()
		self.add_child(self.root)
		self.background_color = '#0b1d28'
		self.tiles = []
		self.selected = []
		self.touched_tile = None
		self.score_label = sk.LabelNode()
		self.score_label.font_name = 'AvenirNext-Regular'
		self.score_label.font_size = 50
		self.score_label.h_align = sk.H_ALIGN_CENTER
		self.score_label.text = '0'
		self.score = 0
		self.game_over = False
		self.game_over_time = 0
		self.add_child(self.score_label)
		self.word_label = sk.LabelNode()
		self.word_label.font_name = 'AvenirNext-Regular'
		self.add_child(self.word_label)
		self.time_label = sk.LabelNode()
		self.time_label.font_name = 'AvenirNext-Regular'
		self.time_label.text = '00:00'
		self.add_child(self.time_label)
		self.start_time = time.time()
		self.overlay = sk.SpriteNode()
		self.overlay.z_position = 3
		self.overlay.color_blend_factor = 1
		self.overlay.color = 'black'
		self.overlay.alpha = 0
		time_up_label = sk.LabelNode()
		time_up_label.font_name = 'AvenirNext-Regular'
		time_up_label.text = 'Time Up!'
		time_up_label.font_size = 72
		time_up_label.h_align = sk.H_ALIGN_CENTER
		self.overlay.add_child(time_up_label)
		self.add_child(self.overlay)
		self.did_change_size(None)
		self.new_game()
	
	def create_tile(self, x, y):
		letter = choice(letter_bag)
		bonus = random() < 0.07
		t = Tile(x, y, letter, '#cef9ff' if bonus else 'white', 2 if bonus else 1)
		return t
		
	def did_change_size(self, old_size):
		x_margin = (self.size[0] - cols * tile_size)/2
		y_margin = (self.size[1] - rows * tile_size)/2 - tile_size/2
		self.root.position = x_margin + tile_size/2, y_margin + tile_size/2
		self.overlay.position = self.size[0]/2, self.size[1]/2
		self.overlay.size = self.size
		if self.size[0] < self.size[1]:
			self.score_label.position = self.size[0]/2, self.size[1] - 100
			self.score_label.font_size = 60
			self.score_label.font_size = 40
			self.word_label.position = self.size[0]/2, self.size[1] - 140
			self.time_label.position = 20, self.size[1] - 100
			self.time_label.h_align = sk.H_ALIGN_LEFT
		else:
			self.score_label.position = x_margin/2, self.size[1] - 100
			self.score_label.font_size = 40
			self.word_label.position = x_margin/2, self.size[1] - 140
			self.word_label.font_size = 24
			self.time_label.position = self.size[0]-20, self.size[1] - 100
			self.time_label.h_align = sk.H_ALIGN_RIGHT
	
	def update(self):
		time_passed = time.time() - self.start_time
		t = max(0, int(game_duration - time_passed))
		self.time_label.text = '{0}:{1:0>2}'.format(t/60, t%60)
		if t == 0 and not self.game_over:
			self.end_game()
	
	def new_game(self):
		if self.game_over:
			sound.play_effect('digital:ZapThreeToneUp')
		for tile in self.tiles:
			tile.remove_from_parent()
		self.tiles = []
		for x, y in product(xrange(cols), xrange(rows)):
			s = self.create_tile(x, y)
			self.tiles.append(s)
			self.root.add_child(s)
		self.game_over = False
		self.start_time = time.time()
		self.score = 0
		self.score_label.text = '0'
		self.overlay.run_action(sk.Action.fade_out())
		self.word_label.text = ''
		self.selected = []
		
	def end_game(self):
		sound.play_effect('digital:ZapThreeToneDown')
		self.game_over = True
		self.game_over_time = time.time()
		self.overlay.run_action(sk.Action.fade_alpha_to(0.7))
	
	def get_selected_word(self):
		return ''.join([t.letter for t in self.selected]).lower()
	
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
			if abs(tile.position - (x, y)) < tile_size/2:
				if tile.alpha < 1:
					continue
				return tile
		return None
	
	def is_neighbor(self, tile1, tile2):
		if (not tile1 or not tile2 or tile1 == tile2):
			return True
		x1, y1 = tile1.x, tile1.y
		x2, y2 = tile2.x, tile2.y
		if x1 == x2:
			return abs(y2-y1) <= 1
		elif x1 % 2 == 0:
			return abs(x2-x1) <= 1 and 0 <= (y2-y1) <= 1
		else:
			return abs(x2-x1) <= 1 and -1 <= (y2-y1) <= 0
	
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
			tile.selected =  (tile in self.selected)
		sound.play_effect('ui:Click1')
		self.update_word_label()
	
	def update_word_label(self):
		word = self.get_selected_word()
		self.word_label.font_color = '#ddffc2' if word in self.words else '#ffcece'
		self.word_label.text = word.upper()
	
	def calc_score(self, word_tiles):
		n = len(word_tiles)
		multiplier = 1
		for tile in word_tiles:
			multiplier *= tile.multiplier
		return int((2 **(n-2)) * 50 * multiplier)
	
	def submit_word(self):
		word = self.get_selected_word()
		if not word:
			return
		if word in self.words:
			sound.play_effect('digital:PowerUp7')
			added_score = self.calc_score(self.selected)
			self.score += added_score
			self.score_label.text = str(self.score)
		else:
			added_score = 0
			sound.play_effect('digital:PepSound4')
			for tile in self.selected:
				tile.selected = False
			self.selected = []
			self.touched_tile = None
		for tile in self.selected:
			tile.run_action(sk.Action.fade_out(0.25))
			tile.run_action(sk.Action.scale_to(0.5, 0.25))
		self.tiles[:] = [t for t in self.tiles if t not in self.selected]
		sorted_selection = sorted(self.selected, key=lambda t: t.y, reverse=True)
		new_tiles_by_col = [0] * cols
		offsets = [0] * len(self.tiles)
		for t in sorted_selection:
			x, y = t.x, t.y
			new_tiles_by_col[x] += 1
			for i, tile in enumerate(self.tiles):
				if tile.x == x and tile.y > y:
					tile.y -= 1
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
		if added_score > 0:
			self.show_points(self.selected[-1].position, added_score)
		self.selected = []
		self.touched_tile = None
		self.update_word_label()
		
	def show_points(self, position, added_score):
		points_bg = sk.SpriteNode(point_bg_tex)
		points_label = sk.LabelNode()
		points_label.text = '+' + str(added_score)
		points_label.h_align = sk.H_ALIGN_CENTER
		points_label.v_align = sk.V_ALIGN_CENTER
		points_bg.position = position
		points_label.font_name = 'AvenirNextCondensed-Regular'
		points_bg.add_child(points_label)
		points_bg.alpha = 0
		fade_out = sk.Action.fade_out(0.5)
		fade_out.timing_mode = sk.TIMING_EASE_IN
		points_bg.run_action(sk.Action.sequence([sk.Action.fade_in(0.25), sk.Action.wait(0.5), fade_out, sk.Action.call(points_label.remove_from_parent)]))
		points_bg.run_action(sk.Action.move_by(0, 100, 1.5))
		self.root.add_child(points_bg)
	
	def touch_began(self, node, touch):
		if self.game_over:
			return
		last_touched_tile = self.touched_tile
		self.touched_tile = self.tile_at(touch.location)
		if last_touched_tile == self.touched_tile:
			self.submit_word()
		elif self.touched_tile:
			self.select_tile(self.touched_tile)
	
	def touch_moved(self, node, touch):
		if not self.game_over:
			self.select_tile(self.tile_at(touch.location))
	
	def touch_ended(self, node, touch):
		if self.game_over:
			if time.time() - self.game_over_time > 2.0:
				self.new_game()
			return
		tile = self.tile_at(touch.location)
		if tile == self.touched_tile:
			self.select_tile(tile)
		else:
			self.submit_word()

def main():
	game = Game()
	scene_view = sk.View()
	scene_view.run_scene(game)
	scene_view.present()

if __name__ == '__main__':
	main()