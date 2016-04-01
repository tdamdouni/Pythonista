'''Executes perspective transformations'''

from PIL import Image
import numpy

def find_coeffs(pa, pb):
	'''Find coefficients for perspective transformation'''
	matrix = []
	for p1, p2 in zip(pa, pb):
		matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
		matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

	A = numpy.matrix(matrix, dtype=numpy.float)
	B = numpy.array(pb).reshape(8)

	res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
	return numpy.array(res).reshape(8)

def transform(startpoints, endpoints, im):
	'''Perform a perspective transformation on an image where startpoints are moved to endpoints, and the image is streched accordingly.'''
	width, height = im.size
	coeffs = find_coeffs(endpoints, startpoints)

	im = im.transform((width, height), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
	return im

def absolutecorners(image):
	'''Return the corners of an image'''
	width, height = image.size
	return [(0, 0), (width, 0), (width, height), (0, height)]
def squarecorners(image):
	'''Return the corners of the biggest square that fits the image'''
	width = min(image.size)
	return [(0, 0), (width, 0), (width, width), (0, width)]
if __name__ == "__main__":
	from random import randint
	im = Image.open('Test_Lenna')
	im.show()
	topleft = (randint(0, 128), randint(0, 128))
	topright = (randint(128, 256), randint(0, 128))
	botright = (randint(128, 256), randint(128, 256))
	botleft = (randint(0, 128), randint(128, 256))

	startpoints = [(0, 0),(256, 0),(256, 256),(0, 256)]
	endponts = [topleft, topright, botright, botleft]
	im2 = transform(startpoints, endponts, im)
	im2.show()