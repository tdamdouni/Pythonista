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
		
class Circle (object):
	def __init__(self, center_point, radius):
		self.center = center_point
		self.radius = radius
		self.diameter = radius * 2
		self.area = (pi * (pow(radius, 2)))
		self.circumference = self.diameter * pi
		
		left = (center_point[0] - radius, center_point[1])
		right = (center_point[0] + radius, center_point[1])
		bottom = (center_point[0], center_point[1] - radius)
		top = (center_point[0], center_point[1] + radius)
		
		self.points = (left, bottom, right, top)
		
class Triangle (object): # a beta version of the upcoming Polygon class.
	def __init__(self, type, angles=None, sides=None, isc_angles=None): # angles in degrees.
		# type can be either "isosceles" or "equilateral" or None for an unspecified trangle (supports less features).
		self.angles = angles
		self.sides = sides
		self.type = type
		
	def find_angle(self):
		if self.type == None:
			added = 0
			empty_angle = self.angles.index(None)
			angles = list(range(0, len(self.angles), 1))
			angles.pop(empty_angle)
			for angle in angles:
				added += self.angles[angle]
			return 180-added
		elif self.type == "equilateral":
			return 60
		elif self.type == "isosceles":
			pass

