# coding: utf-8

# https://gist.github.com/omz/071932322204bcad6063

# Optimized version of the code in this forum post: https://forum.omz-software.com/topic/2850/2-problems-with-shape-nodes-and-sprite-nodes

from scene import *
import random
import ui
import math

def render_bottom_texture(width=100.0):
	left_path = ui.Path()
	left_path.move_to(0, 0)
	left_path.line_to(width/2, width/4)
	left_path.line_to(width/2, 0)
	right_path = ui.Path()
	right_path.move_to(width, 0)
	right_path.line_to(width / 2, 0)
	right_path.line_to(width/2, width/4)
	img_height = width/4
	with ui.ImageContext(width, width/4) as ctx:
		ui.set_color('#009900')
		left_path.fill()
		ui.set_color('#3fb427')
		right_path.fill()
		return Texture(ctx.get_image())

def render_top_texture(width=100.0):
	height = width/2
	top_path = ui.Path()
	top_path.move_to(width / 2, width/2)
	top_path.line_to(width, width/4)
	top_path.line_to(width / 2, 0)
	top_path.line_to(0, width/ 4)
	top_path.line_to(-width / 2, 0)
	with ui.ImageContext(width, height) as ctx:
		ui.set_color('#3aa243')
		top_path.fill()
		return Texture(ctx.get_image())

class HeightTileNode (Node):
	def __init__(self, top_tex, bottom_tex, width, height, position):
		Node.__init__(self, position=position)
		bottom_node = SpriteNode(bottom_tex, parent=self)
		right_wall = SpriteNode(parent=self)
		right_wall.size = (width/2, height)
		right_wall.color = '#3fb427'
		right_wall.anchor_point = (-1, 0)
		right_wall.position = (0, width/8)
		left_wall = SpriteNode(parent=self)
		left_wall.size = (width/2, height)
		left_wall.color = '#009900'
		left_wall.anchor_point = (1, 0)
		left_wall.position = (0, width/8)
		top_node = SpriteNode(top_tex, parent=self)
		top_node.position = (0, height + width/8)

class MyScene (Scene):
	def create_tile(self, height, position, width=100.):
		return HeightTileNode(self.top_tex, self.bottom_tex, width, height, position)

	def setup(self):
		self.width = 100.0
		self.bottom_tex = render_bottom_texture(self.width)
		self.top_tex = render_top_texture(self.width)
		self.map_width = 29
		self.height_map = []
		for i in range(0, self.map_width):
			self.height_map.append([])
			for k in range(0, self.map_width):
				self.height_map[-1].append(random.randint(1, 255))
		self.height_tile_node = Node(position = (700, -50))
		self.height_tile_node.scale = 0.32
		self.height_tile_node.position = (275, 200)
		self.add_child(self.height_tile_node)
		for i in range(len(self.height_map) - 1, -1, -1):
			for k in range(0, len(self.height_map[i])):
				tile_node = self.create_tile(self.height_map[i][k], (k * self.width / 2 + i * self.width / 2 - 738, i * self.width / 4 - k * self.width / 4 + 384), self.width)
				self.height_tile_node.add_child(tile_node)

run(MyScene(), show_fps=True)
