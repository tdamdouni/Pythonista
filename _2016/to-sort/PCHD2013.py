'''Pacman Checkers Hero Deathmatch 2013
A game by Tyler Leite
'''

# This app is made using Pythonista, an iOS application for creating Python programs
# with audio, graphics, and touch input.
# Documentation for Pythonista can be found here: http://omz-software.com/pythonista/docs/ios/

from scene import *
from random import seed, randrange
seed()

#####################
### Tile - ID key ###
### 0 ...... tmp  ###
### 1 ...... wall ###
### 2 ...... air  ###
### 3 ...... edge ###
#####################

class Player:
	def __init__(self, y, x, r,g,b):
		self.y, self.x = y, x
		self.blt = False # Whether the player bombed last turn
		self.r, self.g, self.b = r, g, b
		
	def draw(self):
		fill(self.r, self.g, self.b)
		ellipse(self.x*16 + 1, (27-self.y)*16 + 1, 14, 14)
		
class Bomb:
	def __init__(self, x, y):
		self.y, self.x = y, x
		
class Map:
	def __init__(self, height, width):
		self.height, self.width = height, width
		self.layout = [[0 for x in range(width)] for y in range(height)]
		self.tmp = [[0 for x in range(width)] for y in range(height)]
		self.generations = 2
		self.fill_permill = 355
		self.min_fill = 500*(width-2)*(height-2)/1000
		self.generate()
		
	def fill(self, y, x):
		''' Simple fill algorithm '''
		# Create a queue of unfilled blocs adjacent to current block and fill them
		fill_q = set()
		fill_q.add((y, x))
		while fill_q:
			y, x = fill_q.pop()
			if self.layout[y][x] == 0:
				self.layout[y][x] = 2
				fill_q.add((y-1,   x))
				fill_q.add((y+1,   x))
				fill_q.add((  y, x-1))
				fill_q.add((  y, x+1))
				
				
	def make_random(self):
		for y in range(self.height):
			for x in range(self.width):
				if randrange(1000) <= self.fill_permill:
					self.layout[y][x] = 1
				else:
					self.layout[y][x] = 0
				# Write progress to the tmp array
				self.tmp[y][x] = self.layout[y][x]
				
	def survival_alg(self):
		''' Cycle through the non-edge tiles in the map '''
		for y in range(1, self.height-1):
			for x in range(1, self.width-1):
				count = 0
				# Check a 3x3 square around the current tile for walls
				for i in range(-1, 2):
					for j in range(-1, 2):
						if self.layout[y+i][x+j] == 1:
							count += 1
				# If a '0' is surrounded by 0 or 4+ '1', it turns into a '1' '''
				if (self.layout[y][x] == 0) and ((count > 4) or (count == 0)):
					self.tmp[y][x] = 1
				# If a '1' is surrounded by fewer than 4 '1', it turns into a '0' '''
				elif (self.layout[y][x] == 1) and (count < 4):
					self.tmp[y][x] = 0
		# Finalize the current generation by writing tmp to layout
		for y in range(self.height):
			for x in range(self.width):
				self.layout[y][x] = self.tmp[y][x]
			pass
			
	def fill_edges(self):
		''' Fill the edges of layout with impenetrable walls'''
		for x in range(self.width):
			self.layout[0][x] = 3
			self.layout[self.height-1][x] = 3
		for y in range(self.height):
			self.layout[y][0] = 3
			self.layout[y][self.width-1]    = 3
			
			
	def fill_holes(self):
		''' This isn't the most efficient way to do this, but it works very
		quickly for maps even as large as 1024x1024
		'''
		while True:
			y, x = randrange(self.height), randrange(self.width)
			if self.layout[y][x] == 0:
				self.fill(y, x)
				break
				
	def make_pretty(self):
		air_count = 0
		for y in range(self.height):
			for x in range(self.width):
				if self.layout[y][x] == 2:
					air_count += 1
				elif self.layout[y][x] == 3:
					pass
				else:
					self.layout[y][x] = 1
		return air_count
		
	def draw_ascii(self):
		''' Draw the map with ascii graphics for debugging '''
		# Causes Superlag for some reason
		for y in range(self.height):
			for x in range(self.width):
				if self.layout[y][x] == 1:
					print('+'),
				elif self.layout[y][x] == 2:
					print(' '),
				elif self.layout[y][x] == 3:
					print('#'),
				else:
					print('?'), # Unexpected behavior
			print
			
	def generate(self):
		while True:
			self.make_random()
			for generation in range(self.generations):
				self.survival_alg()
			self.fill_edges()
			self.fill_holes()
			if self.make_pretty() >= self.min_fill:
				#self.draw_ascii()
				break
				
class Game (Scene):
	def setup(self):
		''' like an __init__() '''
		rows, cols = 28, 20
		self.cur_player = randrange(2) + 1
		self.win_player = 0
		self.grid = Map(rows, cols)
		self.shooting = False # Whether the move is shooting instead of moving
		self.players = list()
		
		# Add players
		placed_one = False
		while True:
			# Find an air spot for player1 and another spot for player2
			y, x = randrange(self.grid.height), randrange(self.grid.width)
			tile = self.grid.layout[y][x]
			if tile == 2 and not placed_one:
				self.players[0] = Player(y, x, 0.0,0.0,1.0)
				placed_one = True
			elif tile == 2:
				# Make sure the game won't end in 1 turn
				if abs(self.players[0].y - y) > 2 and abs(self.players[0].x - x) > 2:
					self.players[1] = Player(y, x, 1.0,0.0,0.0)
					break
					
	def move_player(self, direction):
		''' Middleman between touch_began and make_move '''
		if     direction== 'n':
			self.make_move( 0, -1)
		elif direction== 's':
			self.make_move( 0,  1)
		elif direction== 'e':
			self.make_move( 1,  0)
		elif direction== 'w':
			self.make_move(-1,  0)
			
	def shoot_bomb(self, direction):
		''' Find the nearest wall / player in a bomb's path and detonate there
		(don't detonate in a wall, detonate before it
		'''
		# Start the bomb at the current player's location
		if self.cur_player == 1:
			# Check if the player bombed recently
			if self.players[0].blt:
				return
			x = self.players[0].x
			y = self.players[0].y
			self.players[0].blt = True
		elif self.cur_player == 2:
			if self.players[1].blt:
				return
			x = self.players[1].x
			y = self.players[1].y
			self.players[1].blt = True
		boom = Bomb(x, y)
		# Loop in a direction until the bomb hits a wall or overlaps a player
		while True:
			if direction == 'n':
				if self.grid.layout[boom.y-1][boom.x] == 2:
					boom.y -= 1
				else:
					break
			elif direction == 's':
				if self.grid.layout[boom.y+1][boom.x] == 2:
					boom.y += 1
				else:
					break
			elif direction == 'e':
				if self.grid.layout[boom.y][boom.x+1] == 2:
					boom.x += 1
				else:
					break
			elif direction == 'w':
				if self.grid.layout[boom.y][boom.x-1] == 2:
					boom.x -= 1
				else:
					break
			if ((boom.x == self.players[0].x and boom.y == self.players[0].y) or
			(boom.x == self.players[1].x and boom.y == self.players[1].y)):
				break
		# Explosion
		x = boom.x
		y = boom.y
		p1_hit, p2_hit = False, False
		for i in range(-1, 2):
			for j in range(-1, 2):
				if self.grid.layout[y+j][x+i] != 3:
					self.grid.layout[y+j][x+i] = 2
				if self.players[0].x == x+i and self.players[0].y == y+j:
					p1_hit = True
				if self.players[1].x == x+i and self.players[1].y == y+j:
					p2_hit = True
		# Determine the outcome if players are blown up
		if p2_hit and not p1_hit:
			self.win_player = 1
		elif p1_hit and not p2_hit:
			self.win_player = 2
		elif p1_hit and p2_hit:
			self.win_player = 3
		if self.cur_player == 1:
			self.cur_player = 2
		elif self.cur_player == 2:
			self.cur_player = 1
			
	def make_move(self, dx, dy):
		''' Move the player '''
		self.players[cur_player].x += dx
		self.players[cur_player].y += dy
		
		x = self.players[cur_player].x
		y = self.players[cur_player].y
		
		enm_player = (1+cur_player)%2
		
		# End the game if one player melees the other
		if x == self.players[enm_player].x and y == self.players[enm_player].y:
			self.win_player = cur_player
		elif self.grid.layout[y][x] == 2:
			self.players[cur_player].blt = False
			self.cur_player = enm_player
		# Move the player back if he moves into a wall
		else:
			self.players[cur_player].x -= dx
			self.players[cur_player].y -= dy
			
	def touch_began(self, touch):
		''' Called whenever the screen is touched '''
		# Restart on touch if the game is over
		if self.win_player != 0:
			self.setup()
			return
		point = touch.location
		pixWdt = self.grid.width*16.0
		pixHgt = self.grid.height*16.0
		# If the player touches the middle, prepare to shoot rather than move
		if (point.y < pixHgt*0.75 and point.y > pixHgt*0.25 and
		point.x < pixWdt*0.75 and point.x > pixWdt*0.25):
			self.shooting = True
		# Touched the north button
		if (point.y > pixHgt*0.75 and
		point.x > pixWdt*0.25 and point.x < pixWdt*0.75):
			if self.shooting:
				self.shoot_bomb('n')
			else:
				self.move_player('n')
		# Touched the south button
		elif (point.y < pixHgt*0.25 and
		point.x > pixWdt*0.25 and point.x < pixWdt*0.75):
			if self.shooting:
				self.shoot_bomb('s')
			else:
				self.move_player('s')
		# Touched the east button
		elif (point.y > pixHgt*0.25 and point.y < pixHgt*0.75 and
		point.x > pixWdt*0.75):
			if self.shooting:
				self.shoot_bomb('e')
			else:
				self.move_player('e')
		# Touched the west button
		elif (point.y > pixHgt*0.25 and point.y < pixHgt*0.75 and
		point.x < pixWdt*0.25):
			if self.shooting:
				self.shoot_bomb('w')
			else:
				self.move_player('w')
				
	def touch_ended(self, touch):
		self.shooting = False
		
	def draw_checkerboard(self):
		tint(1.0, 1.0, 1.0)
		for y in range(self.grid.height):
			for x in range(self.grid.width):
				if y%2 == x%2:
					image('Blank', x*16, (self.grid.height-1-y)*16, 16, 16)
					
	def draw_walls(self):
		tint(0.5, 0.5, 0.5)
		for y in range(self.grid.height):
			for x in range(self.grid.width):
				tile = self.grid.layout[y][x]
				if tile == 1 or tile == 3:
					image('Blank', x*16+1, (self.grid.height-1-y)*16+1, 14, 14)
		tint(1.0, 1.0, 1.0)
		
	def draw_players(self):
		''' Draw each player if he is alive '''
		if self.win_player == 0 or self.win_player == 1:
			self.players[0].draw()
		if self.win_player == 0 or self.win_player == 2:
			self.players[1].draw()
			
	def draw_text(self):
		tint(1.0, 1.0, 1.0)
		w, h = self.size.w, self.size.h
		font_size = 20
		if self.win_player != 0:
			if self.win_player == 1:
				out_str = 'Game over! Blue Player wins'
				text(out_str, 'GillSans', font_size, 122, h - 20)
			elif self.win_player == 2:
				out_str = 'Game over! Red Player wins'
				text(out_str, 'GillSans', font_size, 120, h - 20)
			else:
				out_str = 'Game over! It\'s a draw.'
				text(out_str, 'GillSans', font_size, 98, h - 20)
		elif self.cur_player == 1:
			out_str = 'Blue Player\'s turn'
			text(out_str, 'GillSans', font_size, 76, h - 20)
		elif self.cur_player == 2:
			out_str = 'Red Player\'s turn'
			text(out_str, 'GillSans', font_size, 74, h - 20)
			
	def draw(self):
		background(0, 0, 0)
		self.draw_checkerboard()
		self.draw_walls()
		self.draw_players()
		self.draw_text()
		
# Always run the game in portrait orientation):
run(Game(), PORTRAIT)

