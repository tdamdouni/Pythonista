# https://forum.omz-software.com/topic/3761/recieving-error-when-deleting-data-from-within-a-list

import random
board = [[],[],[],[],[],[],[],[],[]]
for column in range(9):
	run = True
	while run:
		x = random.randint(1,9)
		if x not in board[column]:
			board[column].append(x)
			for y in range(9):
				if y != column:
					r = board[column].index(x)
					if x in board[y]:
						if r == board[y].index(x):
							del board[column][r]
		if len(board[column]) == 9:
			run = False
print(board)

