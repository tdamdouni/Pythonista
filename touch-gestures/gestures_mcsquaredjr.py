#!python2

# https://gist.github.com/mcsquaredjr/4490985 

# Detect cardinal and diagonal gestures in Pythonista scene

# 8/3/13 created
# Copyright (c) by McSquaredJr.

from __future__ import print_function
from scene import *
from random import random
from colorsys import hsv_to_rgb
import math

'''A demo showing how to detect cardinal and diagonal gestures
using Al Sweigart's moosegesture library (included). Take into 
consideration that Al's library uses a different coordinate system 
with its origin at the top-left corner, due to which it will return
results that should be flipped verically.

The moosegesture also allows to detect compound gestures, not 
included in this demo.
'''


############################################################
#                       CLASS UTILS                        #
############################################################
class Utils(object):
	'''Helper class to compute coordinates on the instruction
	screen
	'''
	@classmethod
	def computeCoords(self, xo, yo, R, pos):
		if pos == 'n':
			xt = xo 
			yt = yo + R
		elif pos == 's':
			xt = xo
			yt = yo - R
		elif pos == 'e':
			xt = xo + R
			yt = yo
		elif pos == 'w':
			xt = xo - R
			yt = yo
		elif pos == 'ne':
			xt = xo + 0.707*R
			yt = yo + 0.707*R
		elif pos == 'nw':
			xt = xo - 0.707*R
			yt = yo + 0.707*R
		elif pos == 'se':
			xt = xo + 0.707*R
			yt = yo - 0.707*R
		elif pos == 'sw':
			xt = xo - 0.707*R
			yt = yo - 0.707*R
		else: 
			print('***Error, incorrect position %s' % (pos))
			xt = None
			yt = None
		return xt, yt
		
	
############################################################
#                       CLASS ARROW	                   #
############################################################
class Arrow(object):
	'''Computes coordinates of an arrow if coorinates of a tip
	and a tail are given
	'''
	def __init__(self, tailX, tailY, tipX, tipY,
	             arrowLength=20):
		#self.layer = layer
		self.tipX = tipX
		self.tipY = tipY
		self.tailX = tailX
		self.tailY = tailY
		self.arrowLength = arrowLength
		self.xs, self.ys = self.__compute()
		
	def __compute(self):
		'''Compute arrow coordinates'''
		dx = self.tipX - self.tailX;
		dy = self.tipY - self.tailY;
		
		theta = math.atan2(dy, dx);
		
		rad = math.radians(35);
		x = self.tipX - self.arrowLength * math.cos(theta + rad)
		y = self.tipY - self.arrowLength * math.sin(theta + rad)
		
		phi2 = math.radians(-35)
		x2 = self.tipX - self.arrowLength * math.cos(theta + phi2)
		y2 = self.tipY - self.arrowLength * math.sin(theta + phi2)
		
		arrowXs = [self.tipX, x, x2]
		arrowYs = [self.tipY, y, y2]
		
		return arrowXs, arrowYs
		
	def draw(self, strokeColor=(0.8, 0.8, 0.8), strokeWidth=4):
		'''Draw the arrow'''
		stroke(strokeColor[0], strokeColor[1], strokeColor[2])
		stroke_weight(strokeWidth)
		line(self.tipX, self.tipY, self.tailX, self.tailY)
		line(self.xs[0], self.ys[0], self.xs[1], self.ys[1])
		line(self.xs[0], self.ys[0], self.xs[2], self.ys[2])       
		                

############################################################
#                       TRACE CLASS                        #
############################################################
class Trace(object):
	def __init__(self, location):
		self.velocity = Size(1, 1)
		self.location = location
		self.hue = 0.8
		self.alpha = 0.8
		
############################################################
#                     TRACESCENE CLASS                     #
############################################################
class TraceScene(Scene):
	def setup(self):
		self.show_instructions = True
		
		self.traces = set()
		self.p_size = 24 if self.size.w > 700 else 12
		self.msg = 'Draw a gesture with your finger'
		# Initial text size
		self.s = 40 if self.size.w > 700 else 17
		self.coords = []
		# Radius within which the arrows are drawn
		# Define parameters
		self.xo = self.size.w/2.0
		self.yo = self.size.h*0.6
		R = 0.35*self.size.w
		# Positions of arrow tips
		pos = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
		
		self.arrows = []
		# Compute coordinates of arrow tips
		for i in range(len(pos)):
			xt, yt = Utils.computeCoords(self.xo, self.yo, R, pos[i])
			self.arrows.append(Arrow(self.xo, self.yo, xt, yt))
		
		self.xt = []	
		self.yt = []
		# Compute coordinates of labels
		for i in range(len(pos)):
			xt, yt = Utils.computeCoords(self.xo, self.yo, 1.1*R, pos[i])
			self.xt.append(xt)
			self.yt.append(yt)
			
	def should_rotate(self, orientation):
		return False
	
	def touch_began(self, touch):
		self.coords = []
		if self.show_instructions:
			self.show_instructions = False
			blend_mode(BLEND_ADD)
		self.coords.append(touch.location.as_tuple())
		try:
			del self.layer
		except AttributeError:
			pass
		
	
	def touch_moved(self, touch):
		
		trace = Trace(touch.location)
		self.traces.add(trace)
		self.coords.append(touch.location.as_tuple())
		
	def touch_ended(self, touch):
		
		self.s = 80/2 if self.size.w > 700 else 40/2
		self.coords.append(touch.location.as_tuple())
		gesture = getGesture(self.coords)
		gesture_dict = {1:'UL', 2:'U', 3:'UR', 
			            4:'L', 5:'None', 6:'R', 
			            7:'LR', 8:'D', 9:'RD'}
		try:
			self.txt = gesture_dict[gesture[-1]]
		except IndexError:
			self.txt = ''
	
	
		fs = 400 if self.size.w > 700 else 100
		self.layer = TextLayer(self.txt, 'Futura', fs)
		self.layer.background = Color(0.14, 0.14, 0.14)
		self.layer.tint = Color(0.8, 0.8, 0.8)
		self.layer.frame.center(*self.bounds.center().as_tuple())                        
		self.layer.animate('alpha', 0.0, duration=1, autoreverse=False, repeat=1)
		
		blend_mode(BLEND_NORMAL)
			
	
	def draw(self):
		background(0.14, 0.14, 0.14)
		
		if self.show_instructions:
			tint(0.7, 0, 0)
			text(self.msg,
			     'Futura', self.s, self.xo, self.yo/.6/4.0)  
			
			lbl = ['U', 'UR', 'R', 'DR', 'D', 'LR', 'L', 'UL']
			ellipse(self.xo-15, self.yo-15, 30, 30)
			fill(0.8, 0.8, 0.8)
			for i in range(len(self.arrows)):
				self.arrows[i].draw() 
				text(lbl[i], 'Futura', self.s, self.xt[i], self.yt[i])
			        
		try:     
				
			self.layer.update(self.dt)
			self.layer.draw()
			
		except AttributeError:
				pass
		
		dead = set()
		for trace in self.traces:
			r, g, b = (1, 0, 0)
			a = trace.alpha
			tint(r * a, g * a, b * a, a)
			x, y = trace.location.as_tuple()
			s = (2 - a) * self.p_size
			image('White_Circle', x - s/2, y - s/2, s, s)
			trace.alpha -= 0.02
			trace.hue += 0.02
			trace.location.x += trace.velocity.w
			trace.location.y += trace.velocity.h
			if trace.alpha <= 0:
				dead.add(trace)
		self.traces -= dead

#--------------------------------------------------------------------------
"""
"MooseGesture 0.1" a mouse gestures recognition library.
Al Sweigart al@coffeeghost.net
http://coffeeghost.net/2011/05/09/moosegesture-python-mouse-gestures-module

Usage:
	import moosegesture
	gesture = moosegesture.getGesture(points)

Where "points" is a list of x, y coordinate tuples, e.g. [(100, 200), (1234, 5678), ...]
getGesture returns a list of integers for the recognized mouse gesture. The integers
correspond to the 8 cardinal and diagonal directions:

  up-left    up   up-right
		 7   8   9

	left 4       6 right

		 1   2   3
down-left   down  down-right

Second usage:
	strokes  = [2, 4, 6]
	gestures = [[2, 4, 2], [2, 6, 9]]
	gesture = moosegesture.findClosestMatchingGesture(strokes, gestures)

	gesture == [2, 4, 2]

Where "strokes" is a list of the directional integers that are returned from
getGesture(). This returns the closest resembling gesture from the list of
gestures that is passed to the function.

The optional "tolerance" parameter can ensure that the "closest" identified
gesture isn't too different.


Explanation of the nomenclature in this module:
	A "point" is a 2D tuple of x, y values. These values can be ints or floats,
	MooseGesture supports both.

	A "point pair" is a point and its immediately subsequent point, i.e. two
	points that are next to each other.

	A "segment" is two or more ordered points forming a series of lines.

	A "stroke" is a segment going in a single direction (one of the 8 cardinal or
	diagonal directions: up, upright, left, etc.)

	A "gesture" is one or more strokes in a specific pattern, e.g. up then right
	then down then left.


############################################################
#                       MOOSEGESTURE                       #
############################################################

# Copyright (c) 2011, Al Sweigart
# All rights reserved.
#
# BSD-style license:
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the MooseGesture nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY Al Sweigart "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Al Sweigart BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from math import sqrt
from sys import maxsize

# This is the minimum distance the mouse must travel (in pixels) before a
# segment will be considered for stroke interpretation.
_MIN_SEG_LEN = 60

# The integers-to-directions mapping matches the keypad:
#   7 8 9
#   4   6
#   1 2 3
DOWNLEFT = 1
DOWN = 2
DOWNRIGHT = 3
LEFT = 4
RIGHT = 6
UPLEFT = 7
UP = 8
UPRIGHT = 9

_strokesStrings = {1:'DL', 2:'D', 3:'DR', 4:'L', 6:'R', 7:'UL', 8:'U', 9:'UR'}

def getGesture(points):
	# Returns a gesture as a list of directional integers, i.e. [2,6,4] for
	# the down-left-right gesture.
	#
	# The points param is a list of tuples of XY points that make up the user's
	# mouse gesture.
	return _identifyStrokes(points)[0]

def getSegments(points):
	# Returns a list of tuples of integers. The tuples are the start and end
	# indexes of the points that make up a consistent stroke.
	return _identifyStrokes(points)[1]

def getGestureAndSegments(points):
	# Returns a list of tuples. The first item in the tuple is the directional
	# integer, and the second item is a tuple of integers for the start and end
	# indexes of the points that make up the stroke.
	strokes, strokeSegments = _identifyStrokes(points)
	return list(zip(strokes, strokeSegments))

def getGestureStr(strokes):
	# Returns a string of space-delimited text characters that represent the
	# strokes passed in. For example, getGesture([2, 6, 4]) returns "D R L".
	#
	# The strokes parameter is a list of directional integers, like the kind
	# returned by getGesture().
	if len(strokes) and type(strokes[0]) == type(0):
		# points is a list of directional integers, returned from getGesture()
		return ' '.join(_strokesStrings[x] for x in strokes)
	else:
		# points is returned from getGestureAndSegments()
		return ' '.join(_strokesStrings[x] for x in _identifyStrokes(strokes)[0])

def findClosestMatchingGesture(strokes, gestureList, tolerance=maxsize):
	# Returns the gesture in gestureList that closest matches the gesture in
	# strokes. The tolerance is how many differences there can be and still
	# be considered a match.
	if len(gestureList) == 0:
		return None

	strokes = ''.join(strokes)
	gestureList = [''.join(x) for x in gestureList]
	gestureList = list(frozenset(gestureList)) # make a unique list
	distances = {}
	for g in gestureList:
		dist = levenshteinDistance(strokes, g)
		if dist in distances:
			distances[dist].append(g)
		else:
			distances[dist] = [g]
	smallestKey = min(distances.keys())
	if len(distances[smallestKey]) == 1 and smallestKey <= tolerance:
		return [int(x) for x in distances[min(distances.keys())]]
	else:
		return None

def levenshteinDistance(s1, s2):
	# Returns the Levenshtein Distance between two strings as an integer.

	# http://en.wikipedia.org/wiki/Levenshtein_distance
	# The Levenshtein Distance (aka edit distance) is how many changes (i.e.
	# insertions, deletions, substitutions) have to be made to convert one
	# string into another.
	#
	# For example, the Levenshtein distance between "kitten" and "sitting" is
	# 3, since the following three edits change one into the other, and there
	# is no way to do it with fewer than three edits:
	#   kitten -> sitten -> sittin -> sitting
	len1 = len(s1)
	len2 = len(s2)

	matrix = list(range(len1 + 1)) * (len2 + 1)
	for i in range(len2 + 1):
		matrix[i] = list(range(i, i + len1 + 1))
	for i in range(len2):
		for j in range(len1):
			if s1[j] == s2[i]:
				matrix[i+1][j+1] = min(matrix[i+1][j] + 1, matrix[i][j+1] + 1, matrix[i][j])
			else:
				matrix[i+1][j+1] = min(matrix[i+1][j] + 1, matrix[i][j+1] + 1, matrix[i][j] + 1)
	return matrix[len2][len1]

def setMinStrokeLen(val):
	# Set the length (in pixels) a stroke must be to be recognized as a stroke.
	_MIN_SEG_LEN = val

def getMinStrokeLen():
	# Get the minimum segment length.
	return _MIN_SEG_LEN




# Private Functions:

def _identifyStrokes(points):
	strokes = []
	strokeSegments = []

	# calculate lengths between each sequential points
	distances = []
	for i in range(len(points)-1):
		distances.append( _distance(points[i], points[i+1]) )

	# keeps getting points until we go past the min. segment length
	#startSegPoint = 0
	#while startSegPoint < len(points)-1:
	for startSegPoint in range(len(points)-1):
		segmentDist = 0
		curDir = None
		consistent = True
		direction = None
		for curSegPoint in range(startSegPoint, len(points)-1):
			segmentDist += distances[curSegPoint]
			if segmentDist >= _MIN_SEG_LEN:
				# check if all points are going the same direction.
				for i in range(startSegPoint, curSegPoint):
					direction = _getDir(points[i], points[i+1])
					if curDir is None:
						curDir = direction
					elif direction != curDir:
						consistent = False
						break
				break
		if not consistent:
			continue
		elif (direction is not None and ( (not len(strokes)) or (len(strokes) and strokes[-1] != direction) )):
			strokes.append(direction)
			strokeSegments.append( [startSegPoint, curSegPoint] )
		elif len(strokeSegments):
			# update and lengthen the latest stroke since this stroke is being lengthened.
			strokeSegments[-1][1] = curSegPoint
	return strokes, strokeSegments

def _getDir(coord1, coord2):
	# Return the integer of one of the 8 directions this line is going in.
	# coord1 and coord2 are (x, y) integers coordinates.
	x1, y1 = coord1
	x2, y2 = coord2

	if x1 == x2 and y1 == y2:
		return None # two coordinates are the same.
	elif x1 == x2 and y1 > y2:
		return UP
	elif x1 == x2 and y1 < y2:
		return DOWN
	elif x1 > x2 and y1 == y2:
		return LEFT
	elif x1 < x2 and y1 == y2:
		return RIGHT

	slope = float(y2 - y1) / float(x2 - x1)

	# Figure out which quadrant the line is going in, and then
	# determine the closest direction by calculating the slope
	if x2 > x1 and y2 < y1: # up right quadrant
		if slope > -0.4142:
			return RIGHT # slope is between 0 and 22.5 degrees
		elif slope < -2.4142:
			return UP # slope is between 67.5 and 90 degrees
		else:
			return UPRIGHT # slope is between 22.5 and 67.5 degrees
	elif x2 > x1 and y2 > y1: # down right quadrant
		if slope > 2.4142:
			return DOWN
		elif slope < 0.4142:
			return RIGHT
		else:
			return DOWNRIGHT
	elif x2 < x1 and y2 < y1: # up left quadrant
		if slope < 0.4142:
			return LEFT
		elif slope > 2.4142:
			return UP
		else:
			return UPLEFT
	elif x2 < x1 and y2 > y1: # down left quadrant
		if slope < -2.4142:
			return DOWN
		elif slope > -0.4142:
			return LEFT
		else:
			return DOWNLEFT

def _distance(coord1, coord2):
	# Return distance between two points. This is a basic pythagorean theorem calculation.
	# coord1 and coord2 are (x, y) integers coordinates.
	xdist = coord1[0] - coord2[0]
	ydist = coord1[1] - coord2[1]
	return sqrt(xdist*xdist + ydist*ydist)



if __name__ == '__main__':
	run(TraceScene(), orientation=PORTRAIT)






