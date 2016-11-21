# coding: utf-8

# https://forum.omz-software.com/topic/2787/rotating-sprites-to-face-movement-direction-in-scene/6

import math

def angle(a,b):
	"""What angle point 'a' needs in order to face point 'b' """
	x1,y1=a
	x2,y2=b
	
	def cartToPol(x,y):
		"""Convert cartesian coordinates to polar coordinates"""
		radius = math.sqrt(x**2 + y**2) #Pythagorean theorem, a**2+b**2=c**2
		theta = math.atan2(y,x) #Wikipedia told me to do this. Don't ask why. This seems to give a theta between pi and negative pi
		theta += math.pi #Now it's between 0 and 2pi, which is radians
		#theta *= 180/math.pi # node.rotation is in radians. To get degrees, uncomment this.
		
		#0 degrees points straight left.
		return radius,theta
		
	return cartToPol(x2-x1,y2-y1)[1]

