from __future__ import print_function
# http://stackoverflow.com/questions/20540521/new-line-sign-in-list-python

board = [[0]*10 for i in range(10)] # Generate 10 lists filled with 10 0's each.
for x in board:
	print(x) # Print out each [0,0,...0,0] on a new line.
	
#

board = []
for i in range(10):
	for j in range(10):
		board.append("0 ")
	board.append("\n")
print(board)

#

board = []
for i in range(100):
	board.append('0 ')
	# or better: board = ['0 ' for i in range(100)]
print('\n'.join(''.join(board[i:i+10]) for i in xrange(0,100,10)))

print()

board[6] = '4 '
board[18] = 'A '
board[30] = '9 '
board[77] = 'X '
print('\n'.join(''.join(board[i:i+10]) for i in xrange(0,100,10)))

#

board = []
for i in range(10):
	temp = []
	for j in range(10):
		temp.append("0 ")
	board.append(temp)
		
for i in board:
	print(''.join(i))

