# coding: utf-8

# https://forum.omz-software.com/topic/140/crude-hittest

# https://gist.github.com/anonymous/5eb6c63a8e4ab9998e0d

# This is a circle-to-circle based hittest. Used a little nifty math to make it accurate.

# Motion control demo
from scene import *
#from math import sqrt
	
def hitCircles(x1,y1,size1,x2,y2,size2,output=0):
	radius1=size1/2
	radius2=size2/2
	#need to find origins
	x1=x1+radius1
	y1=y1+radius1
	x2=x2+radius2
	y2=y2+radius2
 	#compare the distance to combined radii
 	dx = x2 - x1
	dy = y2 - y1
	radii = radius1 + radius2
	if((dx*dx)+(dy*dy)<radii*radii): output=[dx,dy]
	return output


class MyScene (Scene):
	def setup(self):
		self.x = 0
		self.y = 0
		self.smallx=self.size.w * 0.5
		self.smally=self.size.h * 0.5
	def draw(self):
		background(0, 0, 0)
		fill(1, 0, 0)
		g = gravity()
		textOut='x='+str(round(g.x,1))+' y='+str(round(g.y,1))+' z='+str(round(g.z,1))
		text(textOut,'Futura',40,*self.bounds.center().as_tuple())
		size=((g.z*-1)+2)*10
		self.x += g.x * 10
		self.y += g.y * 10
		self.x = min(self.size.w - size, max(0, self.x))
		self.y = min(self.size.h - size, max(0, self.y))
		ellipse(self.x, self.y, size, size)
		self.smallx+=g.x*2
		self.smally+=g.y*2
		self.smallx = min(self.size.w - size/2, max(0, self.smallx))
		self.smally = min(self.size.h - size/2, max(0, self.smally))
		test=hitCircles(self.smallx,self.smally,size/2,self.x,self.y,size)
		if test:
			self.smallx-=test[0]/5
			self.smally-=test[1]/5
			fill(0,1,1)
		ellipse(self.smallx, self.smally, size/2, size/2)
run(MyScene())