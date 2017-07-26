# -*- coding: utf-8 -*-

# https://gist.github.com/dvalentino/5519057

#
# turtle.py - Turtle Class for Pythonista
#
# When run as a script, the following are demonstrated:
# (a) multiple turtle instances illustrate turtle behaviors
# (b) the classic Koch snowflake is drawn
#
# History:
#               13-Apr-2013   DJValentino   created Turtle Class
#
# Credits:
#       Based upon the turtle graphic module written by OMZ:
#   https://gist.github.com/omz/4413863
#
#
# NOTE:
# The methods implemented from the standard python Turtle Class are:
# Command   Parameters     Description                    Status
# Turtle     None           Creates a new turtle object          DONE
# forward    distance       Moves the turtle forward       DONE
# backward   distance       Moves the turle backward       DONE
# right      angle          Turns turtle by cw "ang" deg   DONE
# left       angle          Turns turtle ccw               DONE
# penup      None           Picks up the turtle's pen      DONE
# pendown    None           Puts down the turtle's pen     DONE
# setheading Angle          Sets curr heading to Angle     DONE (non-std)
# heading    None           Returns curr heading in Deg    DONE
# position   None           Returns current pos as (x,y)   DONE
# goto       x,y            Move the turtle to x,y         DONE
# color      r,g,b          Changes the color of the pen   DONE (non-std)
# penwidth   int Width      Changes the width of the pen   DONE (non-std)
#

from canvas import set_size, draw_rect, draw_line, set_stroke_color, set_line_width
from math import sin, cos, pi
from random import randint, random
from time import sleep

DELAY = 0.0

def reset():
	set_size(512, 512)
	set_line_width(3)
	set_stroke_color(0,0,0)
	draw_rect(0, 0, 512, 512)
	set_line_width(1)
	set_stroke_color(0, 0, 1)
	return True
	
def to_rad(deg):
	return deg * pi/180.0
	
class Turtle(object):

	def __init__(self):
		self.heading = 0.0
		self.pos = (0, 0)
		self.r_color = 0
		self.g_color = 0
		self.b_color = 0
		self.pen_is_down = True
		self.pen_width = 1
		
	def home(self):
		self.heading = 0
		self.pos = (0, 0)
		
	# set the pen color
	# currently, requires r,g,b values from 0.0 - 1.0
	# (should accept text string, e.g., "red", "yellow", etc)
	# (currently, lacking method to get the color)
	def color(self, rd, gn, bl):
		self.r_color = float(rd)
		self.g_color = float(gn)
		self.b_color = float(bl)
		
	# set the pen width (currently, lacking method to get the width)
	def penwidth( self, pw ):
		self.pen_width = int(pw)
		
	# get the current position (currently, set the pos using goto method)
	def position(self):
		return( self.pos )
		
	def forward(self, distance):
		sleep(DELAY)
		to = (self.pos[0] + sin(self.heading) * distance, self.pos[1] + cos(self.heading) * distance)
		if self.pen_is_down:
			set_line_width(self.pen_width)
			set_stroke_color(self.r_color, self.g_color, self.b_color)
			draw_line(self.pos[0], self.pos[1], to[0], to[1])
		self.pos = to
		
	def backward(self, distance):
		sleep(DELAY)
		to = (self.pos[0] - sin(self.heading) * distance, self.pos[1] - cos(self.heading) * distance)
		if self.pen_is_down:
			set_line_width(self.pen_width)
			set_stroke_color(self.r_color, self.g_color, self.b_color)
			draw_line(self.pos[0], self.pos[1], to[0], to[1])
		self.pos = to
		
	def right(self, angle):
		self.heading += to_rad(angle)
		
	def left(self, angle):
		self.heading -= to_rad(angle)
		
	def goto(self, x, y):
		self.pos = (x, y)
		
	def setheading(self, angle):
		self.heading = to_rad(angle)
		
	def heading(self):
		return self.heading
		
	def pendown(self):
		self.pen_is_down = True
		
	def penup(self):
		self.pen_is_down = False
		
if __name__ == '__main__':
	# reset the screen
	reset()
	
	# initialize a list of turtles
	num_hatchlings = 10
	
	hatchling = [Turtle() for i in range(num_hatchlings)]
	
	for i in range(num_hatchlings):
		# assign random colors and penwidth
		hatchling[i].color( random(), random(), random() )
		hatchling[i].penwidth( randint(1,3) )
		
		# randomly position and orient each turtle
		hatchling[i].penup()
		hatchling[i].goto( randint(100,400), randint(100,400) )
		hatchling[i].setheading( randint(0,359) )
		hatchling[i].pendown()
		
	# randomly move the turtles using forward() and setheading()
	# (currently, lacking boundary detection)
	for move in range(100):
		for i in range(num_hatchlings):
			hatchling[i].forward( randint(5,10) )
			hatchling[i].setheading( randint(0,359) )
			
	reset()
	
	#
	# Draw the Koch snowflake using forward(), left() and right()
	# (adapted by OMZ from http://commons.wikimedia.org/wiki/Koch_snowflake)
	my_turtle = Turtle()
	my_turtle.color(0, 0, 1)
	my_turtle.goto(200, 100)
	
	koch_flake = 'FRFRF'
	iterations = 5
	for i in range(iterations):
		koch_flake = koch_flake.replace('F', 'FLFRFLF')
	for move in koch_flake:
		if move == 'F':
			my_turtle.forward(100.0 / (3 ** (iterations - 1)))
		elif move == 'L':
			my_turtle.left(60)
		elif move == 'R':
			my_turtle.right(120)

