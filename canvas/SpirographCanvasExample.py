from __future__ import print_function
#Spirograph.py
from math import *
import canvas
canvas.set_size(1024, 768)

import time

COLOR = "#000000"
#root = ui.View()





def rotate(point, angle, center=(0, 0)):
	counterangle = 360 - angle
	while counterangle > 0: counterangle -= 360
	while counterangle < 0: counterangle += 360
	theta = radians(counterangle)
	#Translate point to rotate around center
	translated = point[0]-center[0] , point[1]-center[1]
	#Rotate point
	rotated = (translated[0]*cos(theta)-translated[1]*sin(theta),translated[0]*sin(theta)+translated[1]*cos(theta))
	#Translate point back
	newcoords = (round(rotated[0]+center[0], 1),round(rotated[1]+center[1], 1))
	return newcoords

def createSpiral(arm1, arm2, color):
	"""arm1 and arm2 are pairs of (length, velocity)"""
	
	canvas.begin_path()
	canvas.move_to(512, 684)
	x, y = 0, 0
	len1, step1 = arm1
	len2, step2 = arm2
	global lines
	lines = []
	previousPositions = []

	while step1 > 10 or step2 > 10:
		step1 /= 2
		step2 /= 2

	global run
	run = 1
	iteration = 1
	inarow = 0
	while run:
		
		iteration += 10
		
		point1 = rotate((0,len1), x)
		point2 = map(sum,zip(rotate((0, len2), y), point1))
		p2 = map(sum, zip(point2, (512, 384)))
		#Detection of whether pattern is repeating itself
		if point2 not in previousPositions:
			previousPositions.append(point2)
			inarow = 0
		else:
			inarow += 1

		if inarow >= 5:
			print("Pattern is detected to be repeating itself")
			run = 0


		if x == 0:
			oldpoint2 = point2
		else:
			canvas.add_line(p2[0], p2[1])
		#lines.append( canvas.add_line(point1[0], point1[1]) )
		#lines.append( canvas.add_line(point2[0], point2[1]) )
		oldpoint2 = point2

		x += step1
		if x > 360: x -= 360
		y += step2
		if y > 360: y -= 360

		#for line in lines:
		#	canvas.delete(line)
		lines = []
		time.sleep(0.005)
	canvas.close_path()
	canvas.set_line_width(1)
	canvas.draw_path()

def graph():
	len1 = scale3.get()
	len2 = scale4.get()
	vel1 = scale1.get()
	vel2 = scale2.get()
	createSpiral((len1, vel1), (len2, vel2), thecolor)

createSpiral((150, 2), (150, 7.5), COLOR)