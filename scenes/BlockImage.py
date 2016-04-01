# coding: utf-8
from scene import *

class block (object):
	def __init__(self, image, x, y):
		self.image = image
		self.x, self.y = x, y

class MyScene (Scene):
	def setup(self):
		self.grid = list()
		images = ('PC_Dirt_Block','PC_Stone_Block','PC_Water_Block') * 3
		for i in xrange(9):
			x = block(images, i % 3, i / 3)
			self.grid.append(x)

	def draw(self):
		for block in self.grid:
			image(block.image[0],
			block.x * 25,
			block.y * 25,
			45, 45)
run(MyScene())