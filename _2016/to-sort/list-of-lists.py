from __future__ import print_function
# https://forum.omz-software.com/topic/3188/i-m-just-trying-to-learn-re-learn-and-i-wan-t-to-create-a-2-dimensional-grid-of-objects/5

import random
from pprint import *

def make_grid(height, width): # 'Value' no longer needed
	grid = []
	
	for y in range(height):
		row = []
		grid.append(row)
		
		for x in range(width):
			row.append(MyClass(x))   # I'm not sure why this format works (as opposed to the usual instancename = ClassName() but again, it's what I found in an example.
			
	return grid
	
	
def print_grid(height, width, grid):   # Doesn't currently print in a nice grid fashion but it correctly accesses every object's 'randomnumber' value and prints the information.

	for y in range(height):
		for x in range(width):
			print(grid[y][x].randomnumber, end=' ')
		print("")
		
# EDIT: added the comma to the first print command and the additional print command with the empty quotes in the larger loop to format the grid properly. I feel very clever now :)



class MyClass(object):
	randomnumber = None   # Initializing the variable.
	
	def __init__(self, number):
		self.number = number   # I have no clue what this line is for (or what self.number refers to) but this line was used in an example I found.
		self.randomnumber = random.randint(0, 9)
		
		
		
random.seed()
grid = make_grid(7, 7)
print_grid(7, 7, grid)   # the arguments make it possible to print just a portion of the grid.

# This print function no longer works currently since it won't let me access 'randomnumber' for the entire grid.
# pprint(grid.randomnumber)

# --------------------

# --------------------

class MyClass(object):

	def __init__(self):
		self.randomnumber = random.randint(0, 9)
		
	def __repr__(self):
		return str(self.randomnumber)

# --------------------

