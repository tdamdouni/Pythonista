# https://forum.omz-software.com/topic/4020/draw-ui-path-within-the-coordinate-system-of-a-node

from scene import *

class MyScene (Scene):
	def setup(self):
		sx, sy = self.size.w * .5, self.size.h * .5
		# I would expect the white rect to have its lower left corner
		# at the center of the screen. But it does not, it is sitting
		# on the origin of the node, x and y seem to have no effect.
		self.white = ShapeNode(ui.Path.rect(sx, sy, 200, 200),
		parent=self,
		position=(0, 0))
		# a reference rect as our white rect is kinda off screen
		self.red = ShapeNode(ui.Path.rect(0, 0, 150, 150),
		parent=self,
		fill_color = 'red',
		position=(sx, sy))
		# Here I would expect a line from the right top corner
		# of the red rect going to a point (25, 50) in the
		# top right direction. But again the path is centered
		# on the node and also the y coordinate is being inverted.
		path = ui.Path()
		path.move_to(75,  75)
		path.line_to(sx + 100, sy + 125)
		path.line_width = 3
		self.cyan = ShapeNode(path,
		parent=self.red,
		stroke_color='cyan',
		position=(0, 0))
		
		
if __name__ == '__main__':
	run(MyScene(), show_fps=False)
	
# --------------------

import ui, scene

def texture_from_path(path, fill_color, width, height):
	with ui.ImageContext(width, height) as ctx:
		ui.set_color(fill_color)
		path.fill()
		img = ctx.get_image()
	return scene.Texture(img)
	
# --------------------

def draw_line(self):
	'''
	'''
	if self.line is not None:
		self.line.remove_from_parent()
	minx, miny = None, None
	path = ui.Path()
	path.line_width = 2
	# self is a pythonista node. self.anchors are some phythonista node
	# objects that are children of self. We want to draw a line through all
	# these anchors within the coord system of self.
	for i, anchor in enumerate(self.anchors):
		p = anchor.position
		# get/update the lower left corner minimum
		minx, miny = (p.x if minx is None else min(minx, p.x),
		p.y if miny is None else min(miny, p.y))
		if i == 0: path.move_to(p.x, -p.y)
		else: path.line_to(p.x, -p.y)
	# the offset(position) of our node has to be the lower left corner
	# point plus the center vector of our path
	self.line = ShapeNode(path,
	stroke_color='green',
	fill_color='transparent',
	position = (minx + path.bounds.w * .5,
	miny + path.bounds.h * .5),
	parent=self)
# --------------------

