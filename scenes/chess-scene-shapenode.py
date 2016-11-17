# coding: utf-8

# https://forum.omz-software.com/topic/3610/scene_drawing-help/2

import scene, ui

class Block(scene.ShapeNode):
	def __init__(self, x, y, w, h,
	fill_color='black', parent=None):
		path = ui.Path.rect(0, 0, w, h)
		self.label = None
		self.root = parent
		super(Block, self).__init__(path=path,
		fill_color=fill_color,
		position=(x, y),
		parent=parent)
		
	def touch_began(self, touch):
		if not self.label:
			self.label = scene.LabelNode('♛',
			font=('Helvetica', 40),
			color='green', parent=self.root)
			self.add_child(self.label)
			
class MyScene (scene.Scene):
	def setup(self):
		self.background_color = 'gray'
		colorlist = ['black', 'lightyellow']
		m, n = 8, 8
		w, h = 64, 64
		start_x, start_y = self.size[0]/2-n/2*w, self.size[1]/2 - m/2*h
		self.grid = {}
		for i in range(m):
			for j in range(n):
				x, y = start_x+i*w, start_y+j*h
				self.grid[i,j] = Block(x, y, w, h,
				fill_color=colorlist[(i+j)%2],
				parent=self)
				
	def touch_began(self, touch):
		for i, j in self.grid:
			if (touch.location in (self.grid[i, j].frame)):
				self.grid[i,j].touch_began(touch)
				return
				
scene.run(MyScene(), show_fps=True)

