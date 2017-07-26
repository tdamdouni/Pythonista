# https://forum.omz-software.com/topic/4020/ui-path-coordinate-system/2

import ui, scene
	
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

def texture_from_path(path, fill_color, width, height):
	with ui.ImageContext(width, height) as ctx:
		ui.set_color(fill_color)
		path.fill()
		img = ctx.get_image()
	return scene.Texture(img)
		
if __name__ == '__main__':
	run(MyScene(), show_fps=False)

