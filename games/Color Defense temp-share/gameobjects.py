# coding: utf-8


from button import *
#from main import *


class Map(object):

	def __init__(self, parent):
		
		# Information about the tiles. Width, height, and numbers across and stacked.
		self.tilew = 30
		self.tileh = 30
		self.numx = 22
		self.numy = 12
		
		self.parent = parent
		
		# The width and height of the mapnode itself is calculated based on the tiles.
		self.w = self.tilew * self.numx
		self.h = self.tileh * self.numy
		
		# The important lists. The master map, the shortest path, and tiles which need to be reset.
		self.map = []
		self.shortestpath = []
		self.tilestoreset = []
		
		# Node stuff.
		self.path = ui.Path.rect(0,0 , self.w,self.h)
		self.node = scene.ShapeNode(self.path, color = 'white', position = (7,10))
		self.node.anchor_point = (0,0)

		# Creates the 2D tilemap.
		for y in range(self.numy):
			row = []
			self.map.append(row)
			
			for x in range(self.numx):
				row.append(Tile(self, x,y))
	
		# Unfortunately, you can't identify neighbors until they actually exist. So this loop has to be run AFTER the initialization loop just above.
		for y in range(self.numy):
			for x in range(self.numx):
				self.identify_neighbors(self.map[y][x])

				
		
		# Decide on the location of the start and finish tiles.
		self.start = self.map[5][0]
		self.finish = self.map[6][21]

		# Initialize the values for each of them.
		self.start.type = 1
		self.start.checked = True
		self.start.travel = 0
		self.start.node.color = 'green'
		
		self.finish.type = 2
		self.finish.node.color = 'red'
	
	
		# Create the first path.
		self.pathfinding()

	

	# Does what it says... given a tile, it looks for its neighbors.
	def identify_neighbors(self, tile):
	
		x = tile.x
		y = tile.y
		
		# The important thing is to avoid the boundaries of the map, which is what these checks are for.
		if x > 0:
			tile.left = self.map[y][x-1]
			tile.neighbors.append(tile.left)
		
		if x < self.numx - 1:
			tile.right = self.map[y][x+1]
			tile.neighbors.append(tile.right)

		if y > 0:
			tile.down = self.map[y-1][x]
			tile.neighbors.append(tile.down)
		
		if y < self.numy - 1:
			tile.up = self.map[y+1][x]
			tile.neighbors.append(tile.up)
	
	
	def was_pressed(self, loc):
	
		# I'm pretty proud of this. Since the map is a predictable grid, as long as we know the touch event was somewhere within its boundaries, we
		# can use math to work out which tile was tapped, rather than cycling through EVERY single tile and checking for a touch collision.
		
		# Distance from the edge of the screen to the edge of the tiles.
		bufferx = self.node.position.x
		buffery = self.node.position.y
		
		# Just an intermediate step to do the actual calculation.
		tempx = (loc.x - bufferx)/self.tilew
		tempy = (loc.y - buffery)/self.tileh
		
		
		# We start with a pixel coordinate, position.x/y may equal say (345,221). Once it runs through the above math, it'll
		# come out as a number somewhere between 0 and numx/numy. but it'll be a float value like 2.8 or 11.2. Each integer range (2.0 - 2.9 for example)
		# represents one tile on the map so all you have to do is round down.
		
		# The following is the magic math which rounds down. Math.trunc() takes a float and 'truncates' it down to its integer value. This gives us a solid (x,y) coordinate to use.
		x = math.trunc(tempx)
		y = math.trunc(tempy)
		
		# Make sure x and y are within the bounds of the tilemap. This is a failsafe which can probably be removed in a bit.
		if x >= 0 and x < self.numx:
			if y >= 0 and y < self.numy:
			
				i = self.map[y][x]
				
				# If you tap on a tile, currently it just flips between empty and 'wall'. No matter what though, generate a new path.
				if i.type == 0:
					i.add_tower()
					i.tower.node.color = self.parent.colornode.color
					i.type = 3
				
				elif i.type == 3:
					i.remove_tower()
					i.type = 0

				self.pathfinding()

				if len(self.shortestpath) == 0:
					i.type = 0
					i.remove_tower()
					self.pathfinding()



	# Don't delete this, main.py expects it to be here.
	def press_done(self):
		pass
	

	
	def reset_map(self):
		
		# Tilestoreset contains only those tiles which have been altered, for slight efficiency. The less tiles were checked, the faster it is.
		for i in range(len(self.tilestoreset)):
			
			# Reset travel, checked, and label.
			self.tilestoreset[i].travel = (self.numx * self.numy)
			self.tilestoreset[i].checked = False
			self.tilestoreset[i].label.text = ""
			
			# If it was an empty tile, make sure it's grey (rather than pink).
			if self.tilestoreset[i].type == 0:
				#self.tilestoreset[i].node.color = 'grey'
				pass
		
		# Delete the reset list.
		del self.tilestoreset[:]

		# Reset the correct information for the start tile.
		self.start.travel = 0
		self.start.checked = True
		
		iz = len(self.shortestpath) - 1
		for i in range(1, iz):
			self.shortestpath[i].remove_path_tile()
	
		del self.shortestpath[:]
	
	
	'''
	def greedy_first(self, current):
	
		current = current
		next = current
		
		blocked = False
		foundfinish = False
		frontier = []
		
		while blocked == False and foundfinish == False:
	
			if self.finish.x < current.x: # Left
				if current.left.type < 3 and current.left.checked == False:
				
					current.left.travel = current.travel + 1
					current.left.checked = True
					frontier.append(current.left)
					self.tilestoreset.append(current.left)
					next = current.left
		
					if current.left.type == 2:
						foundfinish = True
		
			elif self.finish.x > current.x: # Right
				if current.right.type < 3 and current.right.checked == False:
				
					current.right.travel = current.travel + 1
					current.right.checked = True
					frontier.append(current.right)
					self.tilestoreset.append(current.right)
					next = current.right
					
					if current.right.type == 2:
						foundfinish = True
		
			elif self.finish.y < current.y: # Down
				if current.down.type < 3 and current.down.checked == False:
				
					current.down.travel = current.travel + 1
					current.down.checked = True
					frontier.append(current.down)
					self.tilestoreset.append(current.down)
					next = current.down

					if current.down.type == 2:
						foundfinish = True
		
			elif self.finish.y > current.y: # Up
				if current.up.type < 3 and current.up.checked == False:
				
					current.up.travel = current.travel + 1
					current.up.checked = True
					frontier.append(current.up)
					self.tilestoreset.append(current.up)
					next = current.up

					if current.up.type == 2:
						foundfinish = True
					
			if next == current:
				blocked = True
				frontier.append(current)
			
			print ("greedy:",current.x,current.y)
			current = next
			
		return frontier, foundfinish
	'''

	def pathfinding(self):
		
		# Reset the map's pathfinding variables before starting, and erase the shortestpath list.
		self.reset_map()
		
		# Frontier and frontier2 are used together. Frontier holds the 'current' frontier, frontier2 holds the upcoming one. At the end of the cycle, frontier adopts frontier2.
		frontier = [self.start]
		frontier2 = []
		
		# These are the status of the pathfinder. If finish is found or the algorithm is trapped, stop the process.
		foundfinish = False
		trapped = False
		

		
		# The ground-level loop. Continue until one condition has changed.
		while foundfinish == False and trapped == False:
			
			# Look at each frontier tile, one at a time.
			for i in range(len(frontier)):
				
				current = frontier[i]
				neighbors = current.neighbors
				
				# Look at the neighbors for the current frontier tile.
				for j in range(len(neighbors)):
				
					# If neighbor is not a tower, and it hasn't already been checked, and the finish hasn't been found:
					if neighbors[j].type < 3 and neighbors[j].checked == False and foundfinish == False:
					
						# Give it its travel value, mark it checked, add it to the next frontier, and mark it for resetting.
						neighbors[j].travel = (frontier[i].travel + 1)
						neighbors[j].checked = True
						frontier2.append(neighbors[j])
						self.tilestoreset.append(neighbors[j])
						
						# Debugging.
						neighbors[j].label.text = "{0}".format(neighbors[j].travel)
						
						# If it was the finish tile:
						if neighbors[j].type == 2:
						
							# Set foundfinish to true, and change j and i to their final value to quit their loops immediately.
							foundfinish = True
							j = range(len(neighbors) - 1)
							i = range(len(frontier) - 1)
		
			# Pass frontier2 off to frontier, clear both lists.
			del frontier[:]
			frontier = frontier2[:]
			del frontier2[:]
			
			# We're in the main loop. If frontier is empty, we must be trapped so mark it.
			if len(frontier) == 0:
				trapped = True

		# Only generate a path if we're not trapped.
		if trapped == False:
			self.generate_path()



	# This method has to walk backwards from the finish tile to create the path.
	def generate_path(self):
		
		# Intialize by starting at the finish. Append it to the shortestpath list.
		current = self.finish
		self.shortestpath.append(self.finish)
	
		# We only need to run this for as many times as the value of travel for the finish tile.
		for i in range(self.finish.travel):
			
			# Used as part of a 'fake' loop at the next level. Nextfound is a checking variable.
			j = 0
			nextfound = False
			
			# As long as the next tile hasn't yet been found...
			while nextfound == False:
				
				selected = current.neighbors[j]
				
				# If the selected tile's travel value is less than the current one:
				if selected.travel < current.travel:
				
					# Add it to the list, make it the current tile, mark nextfound as true.
					self.shortestpath.append(selected)
					current = selected
					nextfound = True
				
				# Increment indefinitely.
				j += 1

		# Reverse the direction of the list (the tiles were added from finish to start, backwards. Draw the path.
		self.shortestpath.reverse()
		self.draw_path()
	
	
	# This method is currently just for visual debugging.
	def draw_path(self):
		
		for i in range(len(self.shortestpath)):
			
			#self.shortestpath[i].label.text = "[{0}]".format(i)
			#self.shortestpath[i].node.color = 'pink'
			self.shortestpath[i].add_path_tile()
			self.shortestpath[i].label.text = ""

		self.shortestpath[0].remove_path_tile()
		self.shortestpath[i].remove_path_tile()

		#self.start.node.color = 'green'
		#self.finish.node.color = 'red'



class Tile(object):

	def __init__(self, parent, x,y):
	
		# The (x,y) coordinates of this tile on the map.
		self.x = x
		self.y = y
		
		self.pathtile = False
		self.tower = False
		
		self.tilew = parent.tilew
		self.tileh = parent.tileh
		
		# The actual pixel position of each tile.
		self.posx = x * parent.tilew
		self.posy = y * parent.tileh
		
		# The middle of each tile.
		self.midx = parent.tilew/2
		self.midy = parent.tileh/2
		
		# Node stuff.
		self.path = ui.Path.rect(0,0 , parent.tilew, parent.tileh)
		self.node = scene.ShapeNode(self.path, color = 'grey', stroke_color = 'cyan', position = (self.posx, self.posy))
		self.node.color = 'grey'
		self.node.anchor_point = (0,0)
		self.node.line_width = 1
		parent.node.add_child(self.node)
		
		# Each tile is aware of its neighbors, as individuals and as a list.
		self.left = False
		self.right = False
		self.down = False
		self.up = False
		self.neighbors = []
		
		# Types:
		#	0 = Empty		1 = Start
		#	2 = Finish		3 = Tower
		self.type = 0
		
		# Used for pathfinding. travel = the total number of tiles on the map.
		self.checked = False
		self.travel = (parent.numx * parent.numy)
		
		# Only for debugging right now, but each tile has a label.
		self.label = scene.LabelNode("", font = ('helvetica',8))
		self.label.position = (parent.tilew/2,parent.tileh/2)
		self.node.add_child(self.label)
	
	
	
	def add_tower(self):
	
		self.tower = Tower(self)
	
	def remove_tower(self):
	
		self.tower.node.remove_from_parent()
		self.tower = False
	
	
	def add_path_tile(self):
	
		self.pathtile = PathTile(self)
	
	def remove_path_tile(self):
	
		self.pathtile.node.remove_from_parent()
		self.pathtile = False
	

	def was_pressed(self, loc):
		pass

	def press_done(self):
		pass


class Tower(object):

	def __init__(self, parent):

		self.x = parent.x
		self.y = parent.y

		self.path = ui.Path.rect(0,0 , 20,20)
		self.node = scene.ShapeNode(self.path, color = 'green', stroke_color = 'black', position = (parent.midx + 0.5,parent.midy + 0.5))
		#self.node.anchor_point = (0,0)
		self.node.line_width = 2
		parent.node.add_child(self.node)


class PathTile(object):

	def __init__(self, parent):

		self.x = parent.x
		self.y = parent.y

		self.path = ui.Path.rect(0,0 , 10,10)
		self.node = scene.ShapeNode(self.path, color = (0.45,0.45,0.45), position = (parent.midx + 0.5,parent.midy + 0.5))
		self.node.rotation = 0.72
		#self.node.line_width = 2
		parent.node.add_child(self.node)


class Wave(object):

	def setup(self):
		pass


class Creep(object):

	def setup(self):
		pass
