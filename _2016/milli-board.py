# https://forum.omz-software.com/topic/3813/set_needs_display-explained

import ui

class Player(ui.View):
	def __init__(self, pos, color):
		#self.bring_to_front()
		print(pos)
		self.xpos, self.ypos = pos
		self.color = color
	def draw(self):
		ui.set_color(self.color)
		self.piece = ui.Path.oval(self.xpos, self.ypos, 50, 50)
		self.piece.fill()
		
class Board(ui.View):
	def __init__(self):
		self.height, self.width = 500, 500
		self.background_color = 0.8, 0.7, 0.5
		self.name = "Mill"
		self.positions = []
		
	def draw(self):
		ui.set_color('black')
		upper = int(self.width//2-50)
		lower = int(self.width//4-25)
		for x, size in zip(range(upper, -1, -lower), range(lower, 501, upper)):
			if x == 0:
				x += 20
				size -= 40
			rect = ui.Path.rect(x, x, size, size)
			rect.line_width = 10
			rect.stroke()
		def strokeLine(fx, fy, tx, ty):
			line = ui.Path()
			line.move_to(fx, fy)
			line.line_to(tx, ty)
			line.line_width = 5
			line.stroke()
		strokeLine(self.width/2, 20, self.width/2, upper)
		strokeLine(self.width/2, self.height-20, self.width/2, upper+lower)
		strokeLine(20, self.height/2, upper, self.height/2)
		strokeLine(self.width-20, self.height/2, upper+lower, self.height/2)
		
	def touch_began(self, touch):
		black = Player(touch.location, 'black')
		self.add_subview(black)
		
		
v = Board()
v.present('sheet')

