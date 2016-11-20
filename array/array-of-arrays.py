# https://forum.omz-software.com/topic/3188/i-m-just-trying-to-learn-re-learn-and-i-wan-t-to-create-a-2-dimensional-grid-of-objects/5


from pprint import pprint

def make_grid(num_rows, num_cols, value=None):
	grid = []
	for y in range(num_rows):
		row = []
		grid.append(row)
		for x in range(num_cols):
			row.append(value)
	return grid
	
grid = make_grid(6, 4)
grid[2][3] = 'hello'
grid[3][3] = 'world'
pprint(grid)

# --------------------

grid = [[None for col in range(4)] for row in range(6)]

# --------------------

