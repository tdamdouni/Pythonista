# https://forum.omz-software.com/topic/3769/sudoku-crashes-my-ipad

import random
class game(object):
	def __init__(self):
		self.found = False
		self.board = list([[0] for i in range(9)] for i in range(9))
		for column in range(0,9):
			for row in range(0,9):
				run = True
				while run:
					x = random.randint(1,9)
					n = column
					o = x
					p = row
					self.found = False
					if x not in self.board[column]:
						for y in range(9):
							self.check = True
							if y != column:
								if self.board[y][row] == x:
									self.check = False
					else:
						self.check = False
					if self.check == True:
						self.board[column][row] = x
						run = False
		print(self.board)
game()
