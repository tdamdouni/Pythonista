# http://jerrekedb.deviantart.com/gallery/33102100

""" Spirograph drawing
    Created on 8/10/2011

    Author: Jeroen De Busser
"""

import turtle
import math # Needed for the FancyCircleRing
import random


def reset_turtle(t):
	'''Resets the turtle t'''
	t.reset()
	t.speed(0)
	t.hideturtle()
	
	
def init_turtle():
	'''Returns a turtle in an initialized turtle environment'''
	window = turtle.Screen()
	window.bgcolor('black')
	window.tracer(0)
	alex = turtle.Turtle()
	reset_turtle(alex)
	return alex
	
	
def __draw_circle(t, distance, sz, n):
	"""Draws a circle at a distance from the current position with a size of sz
	If n is not equal to None, it will draw a regular polygon with n corners
	"""
	# Get to the place where the circle must be drawn
	t.fd(distance)
	t.right(90) # Make sure the circle is at distance from the center
	
	# Draw the circle
	t.down()
	t.circle(sz, 360, n)
	t.up()
	
	# return to the center
	t.left(90)
	t.backward(distance)
	
	
def __draw_ring(t, rsz, rlist, csz, a_circles, a_corners):
	""" Draw a ring with the radii rlist of len(rlist) circles(of size csz) with turtle t
	If a_corners is not None, regular polygons with a_corners corners will be drawn instead of circles
	"""
	for i in rlist:
		__draw_circle(t, rsz*i, csz, a_corners)
		t.left(360/a_circles)
		
		
def range_list(n, amp=0, period=0, phase=0):
	""" Return a list of size n containing factors for the radii of DrawCircleRing. If only given an amount of circles, this function will return a list filled with 1.0
	amp, period and phase are the arguments for a sinus function to draw more complicated patterns than circles, and their default values are chosen to result in a normal spirograph
	"""
	factors = []
	for i in range(n):
		factors.append(amp * math.sin(period * i / n * 2 * math.pi + phase) + 1)
	return factors
	
	
def random_color_list(n):
	""" Make a list of n randomly chosen color tuples """
	colors = []
	for i in range(n):
		colors.append( ( random.random(), random.random(), random.random() ) )
	return colors
	
	
def draw_spirograph(t, ring_t, circle_t, r_list=None):
	""" Make turtle t draw a spirograph with him starting in the center
	Parameters:
	t: the turtle
	ring_t: a tuple or list in this schematic:
	ring_t[0]: radius of the innermost ring
	ring_t[1]: radius of the outermost ring
	ring_t[2]: amount of rings
	ring_t[3]: a list of colors. Can either exist of tuples holding r,g,b values or color names.
	Its length should be equal to ring_t[2]
	circle_t: a tuple/list following this schematic:
	circle_t[0]: radius of the circles in the innermost ring
	circle_t[1]: radius of the circles in the outermost ring
	circle_t[2]: amount of circles/ring
	circle_t[3]: amount of corners. Set to None if you want to draw circles
	r_list: a list, normally constructed with range_list()
	It holds factors to be multiplied with the radius of the current ring to get the distance of each circle in the ring from the center.
	It should be of length circle_t[2]
	If not specified, it will be set to range_list(circle_t[2]) and thus result in a normal spirograph
	"""
	# Check if r_list was specified
	if(r_list == None):
		r_list = range_list(circle_t[2])
		
	# Calculate the size difference between each ring(both ring and circle radii)
	ring_size_diff = (ring_t[1] - ring_t[0]) / ring_t[2]
	circle_size_diff = (circle_t[1] - circle_t[0]) / ring_t[2]
	
	t.up() # Make sure the first moving operation won't draw anything
	for i in range(ring_t[2]):
		t.pencolor(ring_t[3][i])
		__draw_ring(t, ring_t[1] - i * ring_size_diff, r_list, circle_t[1] - i * circle_size_diff, circle_t[2], circle_t[3])
	t.down()
	
	
if __name__ == '__main__':

	# Initialization
	random.seed()
	
	# Draw the Spirograph
	draw_spirograph(init_turtle(), (0, 25, 7, ["green", "purple", "magenta", "blue", "yellow", "orange", "red"] ), (10, 150, 50, None) )
	
	# Keep the window from closing too quickly
	input()

