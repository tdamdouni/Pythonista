# Minesweeper game for iOS in Python (requires Pythonista)
# Author: Maurits van der Schee <maurits@vdschee.nl>
# Sprites: http://www.curtisbright.com/msx/

from PIL import Image
from StringIO import *
from base64 import b64decode

from datetime import datetime
from collections import namedtuple

from scene import *
from random import shuffle
from functools import partial

Sprite = namedtuple('Sprite',('name','size'))

class State:
	thinking, playing, lost, won = range(4)

class Game (Scene):
	
	def setup(self):
		self.width = 8
		self.height = 8
		self.bombs = 10
		self.scale = self.calculate_scale()
		self.sprites = self.load_sprites()
		self.layers = self.add_layers()
		self.new_game()
	
	def calculate_scale(self):
		h_scale = int((self.size.w/(self.width))/16)
		v_scale = int((self.size.h/(self.height+3))/16)
		return min(h_scale,v_scale)
	
	def load_sprite(self,image,bounds):
		width = bounds[2]-bounds[0]
		height = bounds[3]-bounds[1]
		size = Size(width*self.scale,height*self.scale)
		name = load_pil_image(image.crop(bounds).resize(size.as_tuple()))
		return Sprite(name,size)
		
	def load_bg_sprite(self,image):
		w = self.width
		h = self.height
		size = Size(w*16+12*2, h*16+11*3+33)
		background = Image.new('RGBA',size,"silver")
		b = [([0,82,12,93],[0,0,12,11]),
		     ([13,82,14,93],[12,0,12+w*16,11]),
		     ([15,82,27,93],[12+w*16,0,12+w*16+12,11]),
		     ([0,94,12,95],[0,11,12,11+33]),
		     ([15,94,27,95],[12+w*16,11,12+w*16+12,11+33]),
		     ([0,96,12,107],[0,11+33,12,11+33+11]),
		     ([13,96,14,107],[12,11+33,12+w*16,11+33+11]),
		     ([15,96,27,107],[12+w*16,11+33,12+w*16+12,11+33+11]),
		     ([0,108,12,109],[0,11+33+11,12,11+33+11+h*16]),
		     ([15,108,27,109],[12+w*16,11+33+11,12+w*16+12,11+33+11+h*16]),
		     ([0,110,12,121],[0,11+33+11+h*16,12,11+33+11+h*16+11]),
		     ([13,110,14,121],[12,11+33+11+h*16,12+w*16,11+33+11+h*16+11]),
		     ([15,110,27,121],[12+w*16,11+33+11+h*16,12+w*16+12,11+33+11+h*16+11]),
		     ([28,82,69,107],[12+4,11+4,12+4+41,11+4+25]),
		     ([28,82,69,107],[12+w*16-4-41,11+4,12+w*16-4,11+4+25])]
		for (s,t) in b:
			background.paste(image.crop(s).resize((t[2]-t[0],t[3]-t[1])),t)
		size = Size(size.w * self.scale, size.h * self.scale)
		background = background.resize(size.as_tuple())
		name = load_pil_image(background)
		return Sprite(name,size)

	def load_sprites(self):
		data ='''
		iVBORw0KGgoAAAANSUhEUgAAAJAAAAB6CAMAAABnRypuAAADAFBMVEUAAACA
		AAAAgACAgAAAAICAAIAAgIDAwMCAgID/AAAA/wD//wAAAP//AP8A//////8Q
		EBARERESEhITExMUFBQVFRUWFhYXFxcYGBgZGRkaGhobGxscHBwdHR0eHh4f
		Hx8gICAhISEiIiIjIyMkJCQlJSUmJiYnJycoKCgpKSkqKiorKyssLCwtLS0u
		Li4vLy8wMDAxMTEyMjIzMzM0NDQ1NTU2NjY3Nzc4ODg5OTk6Ojo7Ozs8PDw9
		PT0+Pj4/Pz9AQEBBQUFCQkJDQ0NERERFRUVGRkZHR0dISEhJSUlKSkpLS0tM
		TExNTU1OTk5PT09QUFBRUVFSUlJTU1NUVFRVVVVWVlZXV1dYWFhZWVlaWlpb
		W1tcXFxdXV1eXl5fX19gYGBhYWFiYmJjY2NkZGRlZWVmZmZnZ2doaGhpaWlq
		ampra2tsbGxtbW1ubm5vb29wcHBxcXFycnJzc3N0dHR1dXV2dnZ3d3d4eHh5
		eXl6enp7e3t8fHx9fX1+fn5/f3+AgICBgYGCgoKDg4OEhISFhYWGhoaHh4eI
		iIiJiYmKioqLi4uMjIyNjY2Ojo6Pj4+QkJCRkZGSkpKTk5OUlJSVlZWWlpaX
		l5eYmJiZmZmampqbm5ucnJydnZ2enp6fn5+goKChoaGioqKjo6OkpKSlpaWm
		pqanp6eoqKipqamqqqqrq6usrKytra2urq6vr6+wsLCxsbGysrKzs7O0tLS1
		tbW2tra3t7e4uLi5ubm6urq7u7u8vLy9vb2+vr6/v7/AwMDBwcHCwsLDw8PE
		xMTFxcXGxsbHx8fIyMjJycnKysrLy8vMzMzNzc3Ozs7Pz8/Q0NDR0dHS0tLT
		09PU1NTV1dXW1tbX19fY2NjZ2dna2trb29vc3Nzd3d3e3t7f39/g4ODh4eHi
		4uLj4+Pk5OTl5eXm5ubn5+fo6Ojp6enq6urr6+vs7Ozt7e3u7u7v7+/w8PDx
		8fHy8vLz8/P09PT19fX29vb39/f4+Pj5+fn6+vr7+/v8/Pz9/f3+/v7///9Q
		NrN6AAAE5UlEQVR4nO2bgZKjIAxAY7ezVu2M//+3pxAgCUHQUnFvzM61QGJ4
		Bgjo7sHrYgKvnkvr+t8Ber9D/YGC9cGJt38+n+afrXdeUP+Lgnrwgno3XFtA
		bwL0eBAiCjSUAf1mgMIESgO9BVDfu69gH4AMCwNi/hCFj4Dh8kB97750oDcD
		QmkJxIfM4TxCnc2hp5eeD1kAYkNGeQ7NIcR5kHoZkJxDv7WAAo4+ZEbCkKFQ
		oLXOgZDn0JARnFZA77ef1kXLngOVDJnjKVz2hUAsIgqQ0yuTmgIVzaFm9Rso
		CzRzITNMl9r2oxCI7DN3kLUfuOTsFSDmLgkEHki3d3oHBB5o238tILvmjb0t
		ArbqQOA2ijpAYI8wplNj75KQtV/KVr82vgyMqRsoY7/S2L3d+XeEByMUzlMG
		aOBAS90CmMxtwgPYkALyDQcjtFg5IiVC/dLzvHYPCOTt6Rz6KhCbQ6vezBnY
		Aorn0GEgoOJXGXh717XVvwZm74AApP9P5hA9lMdARm+BfITCJEoBuc21EhBf
		xvGQRUCR/4+A5CoLfGhvGPA4oq0ybcj6TyIk8pAEkss+ykO1h8w4wG/F3oBA
		3/vEWLJ1pIHk/psDiuwzW0fGfwQUnQcSQPQmN+3Fbp+zj4BkQ2sB8PcCS6XD
		n6VM2/falJSJHwbkBxuGsXNWpkzbQ3kgNuHajpW5vV4OfXUCCK2WzxHQCsu0
		3ZeHIdj4aztgZWGvln1fnYyQTyIrdZctU3tX7tYIkXLOnvrs4ggFI7TZLGsd
		2AiFcs6e+rwj9D9ECNztBOqNMrX3ZbvKoggl7TcjxHJPSR7SyjIPablK5qFg
		zzM1zbxfyMIl9kURSmXeksilIqRfWziHUnOiZG6VtO9eZa5drpqS1VfSvjsP
		uXaZV0ryU0n7HaH/KUKAK5Gfh1LnG2oDiXOP6ic+Y4F+HsrmD5mH9Gy+Pw85
		G5mpBycVz9Q7bRjQeDEB+dgUnp/GM1UEaNalf431VUnJAy0PnCnXH6iix2D3
		uMuBVBPrurLqrwOZzKm7rqTaBQQwrRLeLI31VQSIwqpA9mrjQbqupyKvYCms
		BhQutw6I64oq//aLwypA9HJjFVwvqh/4mfBTqmBaLzWfUqU4fEkeFz4VCMKH
		7BVVWq8Ye/0qKxIogo2BYGJAEwTXMLEISRWJkFBZFk8kgNjdJ4AYNev1iMqy
		4AcDiu/+DCAz82ynP2Y1CSA+ZgeAACCl2sG6C8jZxbNhWu92MjNIUeEsqQuU
		WS/YOmmqjatilQfid5/KQ/5eYyAfoTgPec/KbUiHZJVRniOZOnj+PFNHsM33
		soJMHe13393t83sZejjtPJTf7aV8/cS4cR6KfoHkngTqq4pOjKnLl+urq0qA
		kpe/xjNVAWi8mLA/aBqXH/Jot/GkyaUfo99UfgFoffSFMpmr4WwAmUdfIC9N
		IF2pDeQn+xJ5njeAvFaCdOVEIPLiDdKVUyPkX01CunJyhLBfSFfuCLWJkCEI
		2037CCFQPzeO0JaybR6yL2f7mUfo/Ey9pWwcoR73squssn5WgO48dGfqT4Eu
		GaGLnYdaZmplc215ptY31yL5JhDby8T/KklLTaCKvqoIj9A4imoDoCa9bgg/
		D80XiNDW8aMtkHL8aAwUZ+ob6Aa6geoAhZe1I/+LmkZA5OXxJYDoy+wrAP0D
		7BQA5IVg6IYAAAAASUVORK5CYII=
		'''
		image = Image.open(StringIO(b64decode(data))).convert('RGBA')
		f = partial(self.load_sprite,image)
		sprites = {}
		sprites['numbers'] = map(lambda x: f([x*16,0,x*16+16,16]),xrange(9))
		sprites['icons'] = map(lambda x: f([x*16,16,x*16+16,32]),xrange(8))
		sprites['digits'] = map(lambda x: f([x*12,33,x*12+11,54]),xrange(11))
		sprites['buttons'] = map(lambda x: f([x*27,55,x*27+26,81]),xrange(5))
		sprites['background'] = self.load_bg_sprite(image)
		return namedtuple('Sprites',sprites.keys())(*sprites.values())
	
	def add_layers(self):
		# root layer
		self.root_layer = Layer(self.bounds)
		# background layer
		width = self.sprites.background.size.w
		height = self.sprites.background.size.h
		offset = Point((self.size.w - width)/2,(self.size.h - height)/2)
		bg = Layer(Rect(offset.x,offset.y,width,height))
		bg.image = self.sprites.background.name
		self.add_layer(bg)
		# help variables
		bg_left = offset.x
		bg_right = offset.x+width
		bg_top = offset.y+height
		bg_bottom = offset.y
		# smiley button layer
		width = self.sprites.buttons[0].size.w
		height = self.sprites.buttons[0].size.h
		offset_x = (self.size.w - width)/2
		offset_y = bg_top-(11+4)*self.scale-height
		button = Layer(Rect(offset_x,offset_y,width,height))
		button.image = self.sprites.buttons[0].name
		self.add_layer(button)
		# bomb count layer
		width = self.sprites.digits[0].size.w
		height = self.sprites.digits[0].size.h
		offset_x = bg_left+(12+4+2)*self.scale
		offset_y = bg_top-(11+4+2)*self.scale-height
		bombs = []
		for i in xrange(3):
			x = offset_x+i*(width+2*self.scale)
			count = Layer(Rect(x,offset_y,width,height))
			count.image = self.sprites.digits[0].name
			self.add_layer(count)
			bombs.append(count)
		# time count layer
		width = self.sprites.digits[0].size.w
		height = self.sprites.digits[0].size.h
		offset_x = bg_right-(12+4+2*3)*self.scale-width*3
		offset_y = bg_top-(11+4+2)*self.scale-height
		seconds = []
		for i in xrange(3):
			x = offset_x+i*(width+2*self.scale)
			count = Layer(Rect(x,offset_y,width,height))
			count.image = self.sprites.digits[0].name
			self.add_layer(count)
			seconds.append(count)
		# tile layers
		tile_width = self.sprites.icons[0].size.w
		tile_height = self.sprites.icons[0].size.h
		width = self.width * tile_width
		height = self.height * tile_height
		offset_x = (self.size.w - width)/2
		offset_y = bg_bottom+11*self.scale
		tiles = []
		for i in xrange(self.width * self.height):
			x, y = i % self.width, i / self.width
			x, y = offset_x + x * tile_width, offset_y + y * tile_height
			tile = Layer(Rect(x, y, tile_width, tile_height))
			self.add_layer(tile)
			tiles.append(tile)
		layers = {}
		layers['root'] = self.root_layer
		layers['background'] = bg
		layers['button'] = button
		layers['bombs'] = bombs
		layers['seconds'] = seconds
		layers['tiles'] = tiles
		return namedtuple('Layers',layers.keys())(*layers.values())
	
	def draw(self):
		background(.8,.8,.8)
		self.layers.root.draw()
		self.draw_button()
		self.draw_counts()
		self.draw_tiles()
		
	def draw_counts(self):
		if self.state in [State.thinking, State.playing]:
			bombs_left = self.bombs_left()
			if bombs_left<0:
				self.layers.bombs[0].image = self.sprites.digits[10].name
				for i in xrange(2):
					digit = (abs(bombs_left)/pow(10,i))%10
					self.layers.bombs[2-i].image = self.sprites.digits[digit].name
			else:
				for i in xrange(3):
					digit = (bombs_left/pow(10,i))%10
					self.layers.bombs[2-i].image = self.sprites.digits[digit].name
			seconds_passed = int((datetime.now() - self.start).total_seconds())
			for i in xrange(3):
				digit = (seconds_passed/pow(10,i))%10
				self.layers.seconds[2-i].image = self.sprites.digits[digit].name

	def draw_tiles(self):
		for tile in self.layers.tiles:
			self.draw_tile(tile)
			
	def bombs_left(self):
		marked = 0
		moves = 0
		for tile in self.layers.tiles:
			if tile.marked:
				marked += 1
			if tile.bomb:
				if tile.open:
					self.state = State.lost
			else:
				if not tile.open:
					moves += 1
		if moves == 0:
			self.state = State.won
			return 0
		return self.bombs - marked
	
	def draw_button(self):
		if self.state in [State.thinking, State.playing]:
			self.state = State.thinking
			for tile in self.layers.tiles:
				if not tile.open and tile.selected:
					self.state = State.playing
					break
		if self.layers.button.selected:
			self.layers.button.image = self.sprites.buttons[4].name
		else:
			self.layers.button.image = self.sprites.buttons[self.state].name

	def new_game(self):
		self.state = State.thinking
		self.layers.button.selected = False
		self.start = datetime.now()
		bomb_locations = [True] * self.bombs
		bomb_locations+= [False] * (self.width * self.height - self.bombs)
		shuffle(bomb_locations)
		for i in xrange(len(self.layers.tiles)):
			x, y = i % self.width, i / self.width
			tile = self.layers.tiles[i]
			tile.bomb = bomb_locations[i]
			tile.selected = False
			tile.hold = 0
			tile.marked = False
			tile.open = False
			tile.image = self.sprites.icons[0].name
			tile.score = 0
			for neighbour in self.get_neighbours(tile):
				if bomb_locations[self.layers.tiles.index(neighbour)]:
					tile.score += 1
	
	def get_neighbours(self,tile):
		i = self.layers.tiles.index(tile)
		x, y = i % self.width, i / self.width
		neighbours = ((-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1))
		for (dx,dy) in neighbours:
			if x+dx>=0 and x+dx<self.width and y+dy>=0 and y+dy<self.height:
				n = (y+dy)*self.width+x+dx
				yield self.layers.tiles[n]
					
	def draw_tile(self,tile):
		if tile.open:
			if tile.bomb:
				tile.image = self.sprites.icons[5].name
			else:
				tile.image = self.sprites.numbers[tile.score].name
		else:
			if self.state in [State.thinking, State.playing]:
				if tile.selected:
					tile.hold += 1
				else:
					tile.hold = 0
				if tile.hold == 15:
						tile.marked = not tile.marked
				if tile.marked:
					tile.image = self.sprites.icons[3].name
				elif tile.selected:
					tile.image = self.sprites.icons[1].name
				else:
					tile.image = self.sprites.icons[0].name
			if self.state == State.lost:
				if tile.bomb and not tile.marked:
					tile.image = self.sprites.icons[2].name
				if not tile.bomb and tile.marked:
					tile.image = self.sprites.icons[4].name
			if self.state == State.won:
				if tile.bomb:
					tile.image = self.sprites.icons[3].name

	def touch_tile(self, touch, release):
		for tile in self.layers.tiles:
			tile.selected = touch.location in tile.frame
			if tile.selected and release:
				tile.selected = False
				if not tile.marked and tile.hold<15:
					self.open_tile(tile)

	def open_tile(self,tile):
		tile.open = True
		if tile.score == 0 and not tile.bomb:
			for neighbour in self.get_neighbours(tile):
				if not neighbour.open:
					self.open_tile(neighbour)
							
	def touch_button(self, touch, release):
		button = self.layers.button
		button.selected = touch.location in button.frame
		if button.selected and release:
			self.new_game()
		
	def touch_began(self, touch):
		if self.state in [State.thinking, State.playing]:
			self.touch_tile(touch, False)
		self.touch_button(touch, False)
		
	def touch_moved(self,touch):
		self.touch_began(touch)
	
	def touch_ended(self, touch):
		if self.state in [State.thinking, State.playing]:
			self.touch_tile(touch, True)
		self.touch_button(touch, True)
		
run(Game(),PORTRAIT)
