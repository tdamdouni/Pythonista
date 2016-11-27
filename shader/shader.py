# https://forum.omz-software.com/topic/3274/fast-color-change-animation-of-a-shape

from scene import *
from ui import Path
import math
import random
from colorsys import hsv_to_rgb

YELLOW = 1/6
BLUE = 2/3
S = 24

class Grid(Scene):
	def setup(self):
		width = int(self.bounds.width) // S
		height = int(self.bounds.height) // S
		self.cells = [Cell(i, j, parent=self) for i in range(width) for j in range(height)]
		
	def touch_moved(self, touch):
		for cell in self.cells:
			cell.touched += S/abs(cell.frame.center() - touch.location)**2
			cell.update()
			
class Cell(ShapeNode):
	def __init__(self, i, j, **vargs):
		self.touched = 0
		super().__init__(Path.rect(0, 0, S, S), 'white', position=(i*S, j*S), **vargs)
		
	def cell_color(self):
		scale = min(1, self.touched)
		hue = scale * YELLOW + (1-scale) * BLUE
		return hsv_to_rgb(hue, 1, 1)
		
	def update(self):
		self.fill_color = self.cell_color()
		
if __name__ == '__main__':
	run(Grid(), show_fps=True)

