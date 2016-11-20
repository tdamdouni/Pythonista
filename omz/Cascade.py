# Cascade Game
#
# This is a complete game that demonstrates drawing images
# and text, handling touch events and combining simple drawing
# with layer animations.
#
# The game is also known as "Same Game".
# It may appear simple at first, but getting a good score
# actually requires some strategy.

from scene import *
from random import randint
from sound import load_effect, play_effect
from functools import partial

# These values are adjusted for the current screen size in
# the setup method, changing them here won't have an effect.
tile_size = 40
cols = 8
rows = 10

class Tile (object):
	def __init__(self, image, x, y):
		self.offset = Point() # used for falling animation
		self.selected = False
		self.image = image
		self.x, self.y = x, y
	
	def hit_test(self, touch):
		frame = Rect(self.x * tile_size + self.offset.x,
		             self.y * tile_size + self.offset.y,
		             tile_size, tile_size)
		return touch.location in frame

class Game (Scene):
	def setup(self):
		#Use different sizes on iPad and iPhone:
		global tile_size, cols, rows
		ipad = self.size.w > 700
		tile_size = 64 if ipad else 40
		cols = 12 if ipad else 8
		rows = 12 if ipad else 10
		if not ipad and self.size.h > 480:
			rows += 2 #iPhone 5
		#Preload some sound effects to reduce latency:
		for sound_effect in ['Click_1', 'Error', 'Coin_3']:
			load_effect(sound_effect)
		self.new_game()
	
	def new_game(self):
		#The effects layer is used to display animated text
		#overlays for scores and the game over screen:
		self.effects = Layer(self.bounds)
		images = ['Green_Apple', 'Grapes', 'Tangerine']
		self.score = 0
		self.game_over = False
		self.grid = list()
		for i in xrange(cols * rows):
			tile = Tile(images[randint(0, len(images)-1)],
			            i % cols, i / cols)
			self.grid.append(tile)
	
	def neighbors(self, tile):
		result = []
		if tile is None: return result
		x, y = tile.x, tile.y
		#Check for neighbors with the same image
		#in all 4 directions:
		directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
		for direction in directions:
			neighbor = self.tile_at(x + direction[0],
			                        y + direction[1])
			if neighbor is not None and neighbor.image == tile.image:
				result.append(neighbor)
		return result
	
	def tile_at(self, x, y):
		if x < 0 or y < 0 or x >= cols or y >= rows:
			return None
		return self.grid[y * cols + x]
	
	def touch_began(self, touch):
		play_effect('Click_1')
		for tile in self.grid:
			if tile is not None: tile.selected = False
		for tile in self.grid:
			if tile is None: continue
			if tile.hit_test(touch):
				self.select_from(tile, set())
				break
	
	def touch_ended(self, touch):
		if self.game_over:
			#Start a new game if the current game has ended:
			self.new_game()
			play_effect('Powerup_3')
			return
		#At least 2 tiles have to be removed:
		sel_count = len(filter(lambda(x): x and x.selected,
		                       self.grid))
		if sel_count < 2:
			play_effect('Error')
			for tile in self.grid:
				if tile is not None: tile.selected = False
			return
		#The first tile is 10 points, the second 20, etc.:
		score_added = ((sel_count * (sel_count + 1)) / 2) * 10
		self.score += score_added
		play_effect('Coin_3')
		#Show the added score as an animated text layer:
		score_layer = TextLayer(str(score_added),
		                        'GillSans-Bold', 40)
		score_layer.frame.center(touch.location)
		self.effects.add_layer(score_layer)
		from_frame = score_layer.frame
		to_frame = Rect(from_frame.x, from_frame.y + 200,
		                from_frame.w, from_frame.h)
		score_layer.animate('frame', to_frame, duration=0.75)
		score_layer.animate('alpha', 0.0, delay=0.3,
		                    completion=score_layer.remove_layer)
		#Remove selected tiles:
		for i in xrange(len(self.grid)):
			tile = self.grid[i]
			if tile is None: continue
			if tile.selected:
				self.grid[i] = None
		#Adjust the positions of the remaining tiles:
		self.drop_tiles()
		#If at least one tile has a neighbor with the same image,
		#another move is possible:
		can_move = max(map(len, map(self.neighbors,
		                            self.grid))) > 0
		if not can_move:
			play_effect('Bleep')
			rest = len(filter(lambda x: x is not None, self.grid))
			msg = 'Perfect!' if rest == 0 else 'Game Over'
			#Show an animated 'Game Over' message:
			font_size = 100 if self.size.w > 700 else 50
			game_over_layer = TextLayer(msg, 'GillSans', font_size)
			game_over_layer.frame.center(self.size.w / 2,
			                             self.size.h / 2)
			game_over_layer.alpha = 0.0
			self.effects.add_layer(game_over_layer)
			#When the animation completes, the game_over flag is set,
			#so that the next tap starts a new game:
			completion = partial(setattr, self, 'game_over', True)
			game_over_layer.animate('alpha', 1.0, duration=1.0,
			                        completion=completion)
			game_over_layer.animate('scale_x', 1.2, autoreverse=True,
			                        duration=1.0)
			game_over_layer.animate('scale_y', 1.2, autoreverse=True,
			                        duration=1.0)
	
	def drop_tiles(self):
		new_grid = [None for x in xrange(len(self.grid))]
		shift = 0
		for col in xrange(cols):
			drop = 0
			col_empty = True
			for row in xrange(rows):
				tile = self.tile_at(col, row)
				if tile is None:
					drop += 1
				else:
					col_empty = False
					new_y = tile.y - drop
					new_x = tile.x - shift
					tile.offset.y += tile_size * (tile.y - new_y)
					tile.offset.x += (tile.x - new_x) * tile_size
					tile.x, tile.y = new_x, new_y
					new_grid[new_y * cols + new_x] = tile
			if col_empty:
				shift += 1
		self.grid = new_grid
	
	def select_from(self, tile, visited, count=1):
		#Recursively select all neighboring tiles
		#with the same image:
		tile.selected = True
		visited.add(tile)
		n = self.neighbors(tile)
		for neighbor in n:
			if neighbor in visited: continue
			if neighbor.image == tile.image:
				count = self.select_from(neighbor, visited, count) + 1
		return count
	
	def draw(self):
		background(0, 0.1, 0.2)
		collision = False
		falling = False
		#Adjust the falling animation speed based
		#on the current framerate:
		fall_speed = self.dt * 700
		#Draw all the tiles:
		draw_selected = False
		tint(1.0, 1.0, 1.0)
		for tile in self.grid:
			if tile is None: continue
			if draw_selected != tile.selected:
				tint(1.0, 1.0, 1.0, 0.5 if tile.selected else 1.0)
				draw_selected = tile.selected
			image(tile.image,
			      tile.x * tile_size + tile.offset.x,
			      tile.y * tile_size + tile.offset.y,
			      tile_size, tile_size)
			if tile.offset.y > 0:
				tile.offset.y = max(0.0, tile.offset.y - fall_speed)
				if tile.offset.y == 0.0: collision = True
				falling = True
		#Draw the current score:
		tint(1.0, 1.0, 1.0)
		w, h = self.size.w, self.size.h
		font_size = 60 if self.size.w > 700 else 40
		text(str(self.score), 'GillSans', font_size, w * 0.5, h - 50)
		#Animate shifting empty columns:
		if not falling:
			for tile in self.grid:
				if tile is None: continue
				if tile.offset.x > 0:
					tile.offset.x = max(0.0, tile.offset.x - fall_speed)
					if tile.offset.x == 0: collision = True
		#Play a sound effect if at least one tile has "landed":
		if collision:
			play_effect('Click_1')
		#Update and draw the text effects layer:
		self.effects.update(self.dt)
		self.effects.draw()

#Always run the game in portrait orientation):
run(Game(), PORTRAIT)
