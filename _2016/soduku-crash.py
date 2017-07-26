# https://forum.omz-software.com/topic/3769/sudoku-crashes-my-ipad/6

from scene import *
import random
import numpy as np
class game(Scene):
	def setup(self):
		self.found = False
		self.board = list([[0] for i in range(9)] for i in range(9))
		for column in range(0,9):
			for row in range(0,9):
				run = True
				while run:
					x = random.randint(1,9)
					self.find(column,x,row)
					if self.found == False:
						self.board[column][row] = x
						run = False
		print(self.board)
	def find(self,list,arg,orig):
		n = list
		o = arg
		p = orig
		self.found = False
		if o not in self.board[n]:
			for y in range(9):
				if y != n:
					if self.board[y][p] == o:
						#self.found = True
						pass
		else:
			self.found = True
			
run(game())

