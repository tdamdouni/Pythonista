# https://forum.omz-software.com/topic/3813/set_needs_display-explained/4

import ui
from math import floor

class Player(object):
	def __init__(self, i, j, color):
		self.i, self.j = i, j
		self.xpos, self.ypos = self.i*60+5, self.j*60+5
		self.color = color
		self.piece = None
		
class Board(ui.View):
	def __init__(self):
		self.height, self.width = 400, 400
		self.background_color = 0.8, 0.7, 0.5
		self.name = "Mill"
		self.toggle = True
		self.positions = []
		self.players = []
		self.valid_positions = set([(0,0), (3,0), (6,0),
		(1,1), (3,1), (5,1),
		(2,2), (3,2), (4,2),
		(0,3),(1,3),(2,3),(4,3),(5,3),(6,3),
		(2,4), (3,4), (4,4),
		(1,5), (3,5), (5,5),
		(0,6), (3,6), (6,6)])
		self.occupied = set()
		
	def draw(self):
		ui.set_color('black')
		for i in range(3):
			rect = ui.Path.rect(i*60+20, i*60+20, (3-i)*120, (3-i)*120)
			rect.line_width = 10
			rect.stroke()
		def strokeLine(fx, fy, tx, ty):
			line = ui.Path()
			line.move_to(fx, fy)
			line.line_to(tx, ty)
			line.line_width = 5
			line.stroke()
		strokeLine(200, 20, 200, 140)
		strokeLine(200, 260, 200, 380)
		strokeLine(20, 200, 140, 200)
		strokeLine(260, 200, 380, 200)
		for p in self.players:
			ui.set_color(p.color)
			p.piece = ui.Path.oval(p.xpos, p.ypos, 30, 30)
			p.piece.fill()
			
	def touch_began(self, touch):
		x,y = touch.location
		i = (floor(x)//60)
		j = (floor(y)//60)
		if (i,j) in self.valid_positions and (i,j) not in self.occupied:
			self.occupied.add((i,j))
			color = 'black' if self.toggle else 'gray'
			self.toggle = not self.toggle
			player = Player(i, j, color)
			self.players.append(player)
			self.set_needs_display()
			
v = Board()
v.present('sheet')

