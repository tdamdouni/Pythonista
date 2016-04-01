# coding: utf-8

# https://forum.omz-software.com/topic/2850/2-problems-with-shape-nodes-and-sprite-nodes

# coding: utf-8

from scene import *
import random

class MyScene (Scene):
	
	def create_tile(self, height, position, width = 100):
		left_path = ui.Path()
		left_path.move_to(width / -2, 0)
		left_path.line_to(width / -2, height)
		left_path.line_to(0, height + math.ceil(width / 4))
		left_path.line_to(0, width / 4)
		left_path.line_to(width / -2, 0)
		right_path = ui.Path()
		right_path.move_to(width / 2, 0)
		right_path.line_to(width / 2, height)
		right_path.line_to(0, height + math.ceil(width / 4))
		right_path.line_to(0, math.ceil(width / 4))
		right_path.line_to(width / 2, 0)

		top_path = ui.Path()
		top_path.move_to(width / 2, 0)
		top_path.line_to(width, width / 4)
		top_path.line_to(width / 2, width / 2)
		top_path.line_to(0, width/ 4)
		top_path.line_to(width / 2, 0)

		new_shape_tile = Node(position = position)
		left_face = ShapeNode(left_path, position = (width / -4, height / 2), fill_color = '#3fb427', parent = new_shape_tile)
		right_face = ShapeNode(right_path, position = (width / 4, height / 2), fill_color = '#009900', parent = new_shape_tile)
		top_face = ShapeNode(top_path, position = (0, height + math.floor(width / 8)), fill_color = '#3aa243', parent = new_shape_tile)

		terrain_tile = SpriteNode(texture = new_shape_tile.render_to_texture(), position = (position[0], position[1] + height / 2))

		return(terrain_tile)

	def setup(self):

		self.width = 100
		self.map_width = 30

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

	def update(self):

		pass

run(MyScene(), show_fps=True)

# Let me first try to explain why you're seeing crashes, and then suggest a more efficient method of rendering this effect.

# You're basically creating a new texture for every tile you're rendering. Given that the height of an average tile is about 128 (with a random number between 1 and 255), the average size of each texture on a 2x retina device (like an iPad 4 or Air) will be roughly 200 × 360 = 72,000 pixels. With RGBA color depth, each pixel takes 4 bytes of memory, so this translates to about 280 KB of texture memory per tile. Take 29 × 29 tiles, and you end up with about 235 MB, which is already a lot, take 100×100, and you'd need almost 3 GB, which is far more than even a new iPad can handle, and that's not taking into account that this is actually the minimum you need, the actual numbers are likely higher because of intermediate buffers, memory needed by other apps, Pythonista itself, etc.

# So, how can we optimize this? The first thing I thought of is that you actually need a maximum number of 255 distinct textures, and you could use the same texture for tiles of the same height. This makes the situation a little better, but unfortunately, it's not quite enough, so let's just skip this and look at a more fundamental optimization to reduce the amount of texture memory we need.

# When you look at the shape of each tile, you can see that the tiles of different heights actually have a lot in common, and that you might be able to construct each of them from the same pieces, basically reusing the parts that are identical.

# In fact, each tile, regardless of its height, can be constructed of four pieces, as you can see here:

# Sketch

# (counting the bottom as one, and the left/right wall separately)

# This can be used to your advantage because you need vastly fewer textures by constructing each height tile node of the same pieces. You just have to vary the size of the left/right walls, and the position of the top/bottom pieces.

# Here's a modified version of your code that uses this technique:

# → Height map demo (Gist)

# You'll notice that starting the script is much faster than before, and using a bigger map shouldn't crash anymore.

# However, performance overall is still not quite as good as I'd like. Using your default map size of 29×29 tiles, I get roughly 40 fps on an iPad Air 2 (you'll probably get less on the iPad 4 / Air 1)...

# 3000 nodes in a scene (4 per tile in my implementation) are just a little too much for the scene module to handle at 60 fps, to be honest... There are a couple of minor optimizations you could still apply, but they probably won't help that much. If you really need better performance than this, you would probably need to look at implementing a custom OpenGL shader. That way, you could theoretically render each tile as a single sprite, and you wouldn't actually need any textures, but it's obviously much more complicated than the technique I've shown above.
