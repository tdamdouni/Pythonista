'''Bradley adaptive thresholding. Credit goes to http://stackoverflow.com/a/33092928/4414003, where user rayryeng wrote an implementation much more efficient than mine'''
from __future__ import print_function
import numpy as np
from PIL import Image
import time

def bradley_threshold(image, s=None, t=None):

	# Convert image to numpy array
	img = np.array(image).astype(np.float)

	# Default window size is round(cols/8)
	if s is None:
		s = np.round(img.shape[1]/8)

	# Default threshold is 15% of the total
	# area in the window
	if t is None:
		t = 15.0

	# Compute integral image
	intImage = np.cumsum(np.cumsum(img, axis=1), axis=0)

	# Define grid of points
	rows,cols = img.shape[:2]
	X,Y = np.meshgrid(np.arange(cols), np.arange(rows))

	# Make into 1D grid of coordinates for easier access
	X = X.ravel()
	Y = Y.ravel()

	# Ensure s is even so that we are able to index into the image
	# properly
	s = s + np.mod(s,2)

	# Access the four corners of each neighbourhood
	x1 = X - s/2
	x2 = X + s/2
	y1 = Y - s/2
	y2 = Y + s/2

	# Ensure no coordinates are out of bounds
	x1[x1 < 0] = 0
	x2[x2 >= cols] = cols-1
	y1[y1 < 0] = 0
	y2[y2 >= rows] = rows-1

	# Count how many pixels are in each neighbourhood
	count = (x2 - x1) * (y2 - y1)

	# Compute the row and column coordinates to access
	# each corner of the neighbourhood for the integral image
	f1_x = x2
	f1_y = y2
	f2_x = x2
	f2_y = y1 - 1
	f2_y[f2_y < 0] = 0
	f3_x = x1-1
	f3_x[f3_x < 0] = 0
	f3_y = y2
	f4_x = f3_x
	f4_y = f2_y

	# Compute areas of each window
	sums = intImage[f1_y, f1_x] - intImage[f2_y, f2_x] - intImage[f3_y, f3_x] + intImage[f4_y, f4_x]

	# Compute thresholded image and reshape into a 2D grid
	out = np.ones(rows*cols, dtype=np.bool)
	out[img.ravel()*count <= sums*(100.0 - t)/100.0] = False

	# Also convert back to uint8
	out = 255*np.reshape(out, (rows, cols)).astype(np.uint8)

	# Return PIL image back to user
	return Image.fromarray(out)


if __name__ == '__main__':
	p=Image.open('../Test Images/test.jpg').convert('L')
	print(p.size)
	
	a=time.time()
	bradley_threshold(p).show()
	print(time.time()-a)