# https://forum.omz-software.com/topic/4119/child-nodes-are-not-anchored-within-their-parent-node

"""
CheckersScene contains:
    One CheckersBoard ShapeNode painted White contains:
        64 CheckersSquare ShapeNodes painted Red and Blue
"""

from scene import *

colorWhite = (1, 1, 1)
colorRed   = (1, 0, 0)
colorBlue  = (0, 0, 1)


class CheckersScene(Scene):
	def setup(self):
		self.board = CheckersBoard(self)
		
	def squareAtCenterOfScreen(self):
		theMin = min(self.size.w, self.size.h)
		theRect = Rect(0, 0, theMin, theMin)
		theOffset = abs(self.size.w - self.size.h) / 2
		if self.size.w > self.size.h:
			theRect.x = theOffset # landscape
		else:
			theRect.y = theOffset # portrait
		return theRect
		
		
class CheckersBoard(ShapeNode):
	def __init__(self, parent, inSquaresPerRow = 8):
		x, y, w, h = parent.squareAtCenterOfScreen()
		super().__init__(ui.Path.rect(x, y, w, h), fill_color='white', # anchor_point=(0, 0),
		parent=parent, position=parent.bounds.center())
		# self.anchor_point = (0, 0)
		sq_size = w / inSquaresPerRow
		for i in range(inSquaresPerRow):
			for j in range(inSquaresPerRow):
				frame = (j * sq_size, i * sq_size, sq_size, sq_size)
				theSquare = BoardSquare(self, frame, (i, j))
				
				
class BoardSquare(ShapeNode):
	def __init__(self, parent, frame, inLocation):
		x, y, w, h = frame
		print(frame)
		super().__init__(ui.Path.rect(x, y, w, h), # anchor_point = (0, 0),
		parent=parent, position=(x, y))
		# self.anchor_point = (0, 0)
		odd = (inLocation[0] + inLocation[1]) % 2
		self.fill_color = colorRed if odd else colorBlue
		
		
run(CheckersScene())

