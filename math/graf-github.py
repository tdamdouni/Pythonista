# https://gist.github.com/Seanld/6cad88d6c3f03811f8074455a9dd193d

# Contains functions and tools that make manipulating and working with graphs easy.
# Written by Sean Wilkerson.

from math import *

def distance(p1, p2): # Takes two points and finds the distance between them.
	return sqrt(pow(p2[0]-p1[0], 2) + pow(p2[1]-p1[1], 2))
	
def midpoint(p1, p2):
	midwidth = (p1[0]+p2[0])/2
	midheight = (p1[1]+p2[1])/2
	return (midwidth, midheight)
	
class Rectangle (object): # (tl, bl, br, tr) each are x,y paired tuples.
	# WARNING: This class should be used specifically for PERFECT rectangles. The math only correctly handles rectangles of equal sides. Use the Polygon class for the more advanced stuff.
	def __init__(self, box):
		self.box = box
		self.width = distance(box[1], box[2])
		self.height = distance(box[0], box[1])
		self.area = self.width * self.height
		self.size = (self.width, self.height)
		self.center = (midpoint(box[1], box[2]), midpoint(box[0], box[1]))
		
box = ((5, 11), (5, 5), (10, 5), (10, 11))
rect = Rectangle(box)
print(rect.center)

