# https://omz-forums.appspot.com/pythonista/post/5054332445655040
# https://gist.github.com/polymerchm/08c5be58a8a6ac4c9798
# coding: utf-8

import math
import ui

def getAngle(a,b): # a = start, b = finish
	theta =  math.atan2(b[1]-a[1], b[0]-a[0])
	if theta < 0:
		theta -= math.pi/2
	elif theta >= 0:
		theta += math.pi/2 + math.pi
	return theta
	
def distance(a,b):	
	return math.sqrt(math.pow((b[1]-a[1]),2) + math.pow((b[0]-a[0]),2))
	
def degrees(a):
	return a*180/math.pi

def dot(A,B): # avoids importing full numpy
	if len(A[0]) != len(B):
		raise ValueError('inner dimensions unequal')
	result = []
	for i in range(len(A)):
		row = []
		for j in range(len(B[0])):
			sum = 0
			for k in range(len(B)):
				sum += A[i][k]*B[k][j]
			row.append(sum)
		result.append(row)
	return result
	
	
def ui_draw_arrow(pointA, pointB, lineWidth=1, lineDash=None, phase=None, 
									 headWidth=0.07, headHeight=0.15, pointType=(0,1)):
	''' this method will use the current settings of the ui.draw and draws an arrow from point A to point B
			pointA and pointB are xy tuples
			headWidth and Headheight are proprtionate to the length
			pointType = tupple with (start,end) types 0: none 1: triangle, 2: classic, 3: circle
				for circle, headWidth is taken as relative radius
	'''
		
	def drawHead(origin,end,thisType):
		theta = getAngle(origin,end)
		cs = math.cos(theta)
		ss = math.sin(theta)
		R = [[cs,-ss],[ss,cs]]
		w = distance(origin,end)*headWidth
		h = distance(origin,end)*headHeight
		if thisType == 1:
			initCoords = [[0, w/2, -w/2, 0],
										[0, -h, -h, -h]] # fourth coordinate is where shaft meets head
		elif thisType == 2:
			initCoords = [[0, w/2, 0, -w/2, 0], 
										[0, -h, -h/2, -h, -h/2]]
		elif thisType == 3:
			initCoords = [[0,0],
										[0,-w]]
		else:
			raise ValueError('invalid head type')
		coords = dot(R,initCoords)
		Xs = [x + end[0] for x in coords[0]]
		Ys = [y + end[1] for y in coords[1]]
		XYs = zip(Xs,Ys)
		if thisType == 3:
			arrow = ui.Path.oval(XYs[0][0]-w,XYs[0][1]-w,2*w,2*w)
		else:
			arrow = ui.Path()
			arrow.move_to(XYs[0][0],XYs[0][1])
			for x,y in XYs[:-1] : # last coordinate not used
				arrow.line_to(x,y)
		arrow.fill()
		return(XYs[-1])
		
	if len(pointA) != 2 or len(pointB) != 2:
		raise ValueError('points must both be on length 2')
	startPoint = pointA
	stopPoint = pointB	

	if pointType[0]:
		startPoint = drawHead(pointB,pointA,pointType[0])	
	if pointType[1]:
		stopPoint = drawHead(pointA,pointB,pointType[1])
	
	line = ui.Path()
	line.line_width = lineWidth
	if lineDash and phase:
		line.set_line_dash(lineDash,phase)
	line.move_to(startPoint[0],startPoint[1])
	line.line_to(stopPoint[0],stopPoint[1])
	line.stroke()
			
if __name__ == '__main__':

	center = (200,200)
	with ui.ImageContext(500,500) as ctx:			
		box = ui.Path.rect(0,0,400,400)
		box.line_width = 4
		ui.set_color('black')
		box.stroke()

		testList = [(200,370), (300,300), (370,200), (100,300), (100,200), (60,100), (200,10), (300,100)]			
		for item in testList:
			ui_draw_arrow(center,item, pointType=(1,3),lineWidth=4,headWidth = 0.07)	
		image = ctx.get_image()
		image.show()
	