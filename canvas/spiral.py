#!python2
# coding: utf-8

# https://gist.github.com/The-Penultimate-Defenestrator/ca552fad4225627417d9

from __future__ import print_function
import turtle
t = turtle.Pen()
t.ht()
t.speed(0)
turtle.colormode(255)

rgb = [255, 0, 0]

def progressrainbow(rgb):
	new = []
	r, g, b = rgb
	if b == 0 and r > 0:
		r -= 1
		g += 1
	elif r == 0 and g > 0:
		g -= 1
		b += 1
	elif g == 0 and b > 0:
		b -= 1
		r += 1
	return r, g, b
	
def spiral(angle):
	for x in range(900):
		global rgb
		rgb = progressrainbow(rgb)
		t.pencolor(rgb)
		t.fd(x)
		t.left(angle)
spiral(89)
print("done!")
turtle.getscreen().getcanvas().postscript(file="output.eps")

