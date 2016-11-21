#!python2
# coding: utf-8

# https://gist.github.com/cclauss/6313658

# Pythonista's canvas module's graphics origin (0, 0) is at the bottomLeft. "with flippedDisplay": will temporarily switch the graphics origin to be at the topLeft.

import canvas, scene
from contextlib import contextmanager

@contextmanager
def privateGstate():
	"""Save the canvas.gstate and then restore it when leaving the 'with' clause."""
	canvas.save_gstate()
	try:     yield None
	finally: canvas.restore_gstate()
	
@contextmanager
def privateMatrix():
	"""Save the scene.matrix and then restore it when leaving the 'with' clause."""
	scene.push_matrix()
	try:     yield None
	finally: scene.pop_matrix()
	
@contextmanager
def flippedDisplay():
	"""Flip the display so that the origin is the topLeft instead of the bottomLeft.
	Restore the origin to bottomLeft when leaving the 'with' clause."""
	canvas.save_gstate()
	canvas.scale(1, -1)
	canvas.translate(0, -screenHeight)
	try:     yield None
	finally: canvas.restore_gstate()
	
screenHeight = 512
circleHeight = 128

colorBlue  = (0, 0, 1)
colorGreen = (0, 1, 0)
colorRed   = (1, 0, 0)

def coloredCircle(inColor, inX, inY):
	canvas.set_fill_color(*inColor)
	canvas.fill_ellipse(inX, inY, circleHeight, circleHeight)
	
canvas.clear()
canvas.set_size(screenHeight * 1.42, screenHeight)

with privateGstate():  # Save and then restore the canvas.gstate
	canvas.rotate(89)  # Text on an angle.
	canvas.draw_text('Green on top -->', 154, 0, 'Helvetica', 36)
canvas.draw_text('<-- Red and Blue on bottom', 282, 52, 'Helvetica', 36)

x = 20 + circleHeight
coloredCircle(colorRed, 10, 10)       # Red circle appears at bottom.
with flippedDisplay():  # Change origin to topLeft instead of bottomLeft.
	coloredCircle(colorGreen, x, 10)  # Green circle appears at top.
coloredCircle(colorBlue, x, 10)       # Blue circle appears at bottom.

