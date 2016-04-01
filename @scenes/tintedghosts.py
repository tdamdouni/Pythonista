# coding: utf-8

# https://gist.github.com/offe/7269e9e3cff6ac88b584

# https://forum.omz-software.com/topic/2448/real-time-numpy-and-ghosts

from scene import *
import random
import math
import numpy as np
from colorsys import hsv_to_rgb

PROFILE = False

MODE_STILL = 0								# Don't do anything in update()
MODE_ONLY_CALCULATE = 1				# Only do numpy position updates
MODE_ONLY_COPY_POSITIONS = 2	# Only copy numpy positions into sprites
MODE_FULL = 3									# Calculate positions and copy them into sprites

RUN_MODE = MODE_FULL
MAX_FOR_FULL_FPS = {
	MODE_STILL: 600,
	MODE_ONLY_CALCULATE: 450,
	MODE_ONLY_COPY_POSITIONS: 450,
	MODE_FULL: 350
}

SPRITE_SIZE = 80
NUMBER_OF_SPRITES = MAX_FOR_FULL_FPS[RUN_MODE]
BORDER = 100

def random_within_bounds(bounds):
	return Point(random.uniform(bounds.min_x, bounds.max_x), 
							 random.uniform(bounds.min_y, bounds.max_y))
	
def random_direction():
	a = random.random() * 2 * math.pi
	return Point(math.sin(a), math.cos(a))

def normalize_ndarray(a):
	d = np.sqrt((a*a).sum(1))
	return a/np.expand_dims(d,2)

class MyScene (Scene):
	def setup(self):
		self.background_color = '#313131'
		self.ghosts_node = Node(position=(-BORDER, -BORDER), parent=self)
		self.set_ghosts_node_size()
		self.sprites = [self.new_sprite() for _ in xrange(NUMBER_OF_SPRITES)]
		self.positions = np.random.rand(NUMBER_OF_SPRITES, 2) * self.ghosts_node.size
		self.vels = 0 * self.positions
		self.destination = 0
		self.set_sprite_positions_from_ndarray()
		
	def set_ghosts_node_size(self):
		self.ghosts_node.size = (self.size.width+2*BORDER, self.size.height+2*BORDER)
			
	def new_sprite(self):
		size = random.uniform(0.5, 1)
		sprite = SpriteNode('emj:Ghost',
												size=(SPRITE_SIZE*size, SPRITE_SIZE*size), 
												parent=self.ghosts_node) 
		sprite.color = hsv_to_rgb(random.random(), 0.1, 1.0)
		sprite.alpha = 0.85
		#sprite.z_position = size
		return sprite
	
	def did_change_size(self):
		self.set_ghosts_node_size()
		
# All of the calculations for the movement is done on NumPy ndarrays. The sprite postions end up in self.positions, an ndarray in which each line is the position for a sprite. Then the sprite node positions are updated like this:
	
	def set_sprite_positions_from_ndarray(self):
		ps = self.positions
		for i, sprite in enumerate(self.sprites):
			sprite.position = ps[i]
		
	def update_positions(self):
		self.vels *= 0.8 ** self.dt 
		max_dv = 1000 * self.dt
		#self.vels += np.random.uniform(-max_dv, max_dv, (NUMBER_OF_SPRITES, 2))
		
		# Change velocity of sprites on one side of a random line
		p = random_within_bounds(self.ghosts_node.bbox)
		d = random_direction()
		selected = ((self.positions - p) * d).sum(1) > 0
		self.vels[selected] -= 300 * self.dt * random_direction()
		
		if self.destination:
			destination = self.ghosts_node.point_from_scene(self.destination)
			self.vels -= 1.0 * normalize_ndarray(self.positions - destination)

		self.positions += self.vels * self.dt
		self.positions %= self.ghosts_node.size
	
	def update(self):
		if RUN_MODE in [MODE_ONLY_CALCULATE, MODE_FULL]:
			self.update_positions()
		if RUN_MODE in [MODE_ONLY_COPY_POSITIONS, MODE_FULL]:
			self.set_sprite_positions_from_ndarray()
	
	def touch_began(self, touch):
		self.destination = touch.location
	
	def touch_moved(self, touch):
		self.destination = touch.location
	
	def touch_ended(self, touch):
		self.destination = None

if __name__ == '__main__':
	if PROFILE:
		import cProfile
		import pstats
		cProfile.run('run(MyScene(), show_fps=True)', 'profiling')
		p = pstats.Stats('profiling')
		p.sort_stats('cumulative').print_stats(20)
	else:
		run(MyScene(), show_fps=True)

# Does anyone have any ideas how to increase the number of sprites (SpriteNodes, with same movement, at full frame rate)?

# I was a bit surprised that when I tried doing nothing in the update method I could only get up to 600 sprites at full frame rate. 600 is a lot, but I was still expecting more since almost no python is being executed. Why is that? You can also see in the code that the entire position update calculations in NumPy is about as time consuming as the simple loop to update the nodes' positions. It illustrates the fantastic performance of NumPy with its ndarrays.

# You can also see my failed attempt at profiling a Scene. I guess the work actual work is done after run() has returned, but I can't figure out how to do it instead. Does anyone have an idea how to profile a Scene to figure out where the time is being spent?