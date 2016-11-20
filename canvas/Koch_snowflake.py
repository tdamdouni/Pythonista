# https://gist.github.com/Phuket2/a7557809fa67f4431ccfff6cd3ae54d2

# https://forum.omz-software.com/topic/3284/what-s-with-canvas-in-pythonista-3/19

#turtle.py
# Basic Turtle graphics module for Pythonista
#
# When run as a script, the classic Koch snowflake is drawn as a demo.
# The module can also be used interactively or from other scripts:
# >>> from turtle import *
# >>> right(30)
# >>> forward(100)
# ...

from canvas import set_size, draw_rect, draw_line, set_stroke_color
from math import sin, cos, pi
from time import sleep

heading = 0.0
pos = (0, 0)
pen_is_down = True

DELAY = 0.1

def to_rad(deg):
	return deg * pi/180.0
	
def home():
	global heading, pos
	heading = 0
	pos = (0, 0)
	
def reset():
	set_size(512, 512)
	home()
	set_stroke_color(0, 0, 0)
	draw_rect(0, 0, 512, 512)
	set_stroke_color(0, 0, 1)
	
def forward(distance):
	sleep(DELAY)
	global pos
	to = (pos[0] + sin(heading) * distance, pos[1] + cos(heading) * distance)
	if pen_is_down:
		draw_line(pos[0], pos[1], to[0], to[1])
	pos = to
	
fd = forward

def backward(distance):
	sleep(DELAY)
	global pos
	to = (pos[0] - sin(heading) * distance, pos[1] - cos(heading) * distance)
	if pen_is_down:
		draw_line(pos[0], pos[1], to[0], to[1])
	pos = to
	
bk = backward
back = backward

def right(angle):
	global heading
	heading += to_rad(angle)
	
rt = right

def left(angle):
	global heading
	heading -= to_rad(angle)
	
lt = left

def goto(x, y):
	global pos
	pos = (x, y)
	
setpos = goto
setposition = goto

def setheading(angle):
	global heading
	heading = to_rad(angle)
	
seth = setheading

def pendown():
	global pen_is_down
	pen_is_down = True
	
pd = pendown
down = pendown

def penup():
	global pen_is_down
	pen_is_down = False
	
pu = penup
up = penup

reset()

if __name__ == '__main__':
	# Draw the Koch snowflake
	# (adapted from http://commons.wikimedia.org/wiki/Koch_snowflake)
	setposition(100, 100)
	koch_flake = 'FRFRF'
	iterations = 2
	for i in range(iterations):
		koch_flake = koch_flake.replace('F', 'FLFRFLF')
	for move in koch_flake:
		if move == 'F':
			forward(100.0 / (3 ** (iterations - 1)))
		elif move == 'L':
			left(60)
		elif move == 'R':
			right(120)

