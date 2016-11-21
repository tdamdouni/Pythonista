# iPad Pythonista
from scene import *

class MyScene (Scene):
	
	def factorss(self):
		return [
		[2,2,2,3,3,5],
		[0,2,2,3,3,5],
		[2,2,2,0,3,5],	
		[0,0,2,3,3,5],	
		[2,2,2,3,3,0],
		[0,2,2,0,3,5],		
		[0,0,0,3,3,5],	
		[2,2,2,0,0,5],	
		[0,2,2,3,3,0],
		[0,0,2,0,3,5],	
		[2,2,2,0,3,0],	
		[0,2,2,0,0,5]]
		
	def polygon(self,w,n,dv,x,y,r,size,dist=1.0):
		v = 2*math.pi/n
		if w<0:
			v=-v
		dr = dv/180.0*math.pi
		wr=w/180.0*math.pi
		
		x0=x+1*r*dist*math.sin(wr)
		y0=y+1*r*dist*math.cos(wr)
		
		x1=x+(r*dist-size)*math.sin(wr)
		y1=y+(r*dist-size)*math.cos(wr)
		
		stroke(0,0,0)
		stroke_weight(1)
		line(x,y,x1,y1)
			     
		tint(1,1,1)	
		text("%d"% abs(w),'helvetica',16,
		      x+(dist*r-size-10)*math.sin(wr),
			     y+(dist*r-size-10)*math.cos(wr))
			     
		tint(0,0,0)
			     
		text("%d"% n,'helvetica',16,x0,y0) 
		
		if n>20:
			stroke_weight(1)
		else:
			stroke_weight(2)
		
		for i in range(n):
			stroke(1,1,1)
			if i==n-1:
				stroke(1,1,0)
			if i==0:
				stroke(0,0,0)
			line(x0+size*math.sin((i+0.5)*v+dr),
			     y0+size*math.cos((i+0.5)*v+dr),
			     x0+size*math.sin((i-0.5)*v+dr),
			     y0+size*math.cos((i-0.5)*v+dr))
			
	def circle(self,x,y,r):
		ellipse(x-r,y-r,r+r,r+r)
	
	def setup(self):
		background(0.5,0.5,0.5)
		fill(0.5,0.5,0.5)
		stroke(1,1,1)
		stroke_weight(2)
		size=30
		
		x=768/2
		y=-50+768/2
		r=700/2
		self.circle(x,y,r-60)
		
		stroke_weight(1)
		stroke(1,1,1)
		line(x,y+r-60,x,y)
		stroke(1,1,0)
		line(x,y,x,y-r+60)
		
		tint(1,1,1)
		
		self.polygon(-2,180,90-2,x,y,r,size,1.62)	
		self.polygon(1,360,-90+1,x,y,r,size,1.8)
		self.polygon(3,120,-90+3,x,y,r,size,1.22)	
		self.polygon(-4,90, 90-4,x,y,r,size,1.4)
		self.polygon(5,72,-90+5,x,y,r,size)	
		self.polygon(-6,60,90-6,x,y,r,size)	
		self.polygon(-8,45,90-8,x,y,r,size,1.8)	
		self.polygon(9,40, -90+9,x,y,r,size,1.41)	
		self.polygon(-10,36,90-10,x,y,r,size,1.2)
		self.polygon(12,30,-90+12,x,y,r,size,1.2)
		self.polygon(18,20,-90+18,x,y,r,size)
		self.polygon(-15,24,90-15,x,y,r,size,1.4)	
		self.polygon(-20,18,90-20,x,y,r,size,1.2)
		self.polygon(-30,12,90-30,x,y,r,size)	
		self.polygon(24,15,-90+24,x,y,r,size,1.2)
		self.polygon(36,10,-90+36,x,y,r,size,1.2)	
		self.polygon(-40,9,90-40,x,y,r,size,1.2)
		self.polygon(72,5,-90+72,x,y,r,size)
		self.polygon(120,3,-90+120,x,y,r,size)
		self.polygon(60,6,-90+60,x,y,r,size)
		self.polygon(45,8,-90+45,x,y,r,size)
		self.polygon(-72,5,90-72,x,y,r,size)
		self.polygon(-120,3,90-120,x,y,r,size)
		self.polygon(-60,6,90-60,x,y,r,size)
		self.polygon(-45,8,90-45,x,y,r,size)	
		self.polygon(90,4,-90+90,x,y,r,size)
		self.polygon(-90,4,-90+90,x,y,r,size)
		
		tint(0.2,0.2,0.2)
		text ("christer nilsson 2013",'helvetica',12,58,8)			
		text ("unit circle",'helvetica',32,600,900)	
		text ("turn left",'helvetica',32,300,200)	
		text ("turn right",'helvetica',32,480,200)
		
		for i,n in enumerate([1,2,3,4,5,6,8,9,10,12,15,18]):
			factors=(self.factorss())[i]
			y0=1000-20*i-20
			tint(0.3,0.3,0.3)
			text( "%d" % n,'helvetica',16,25,y0)
			text( "%d" % (360/ n),'helvetica',16,175,y0)
			tint(1,1,1)
			for j,m in enumerate(factors):
				x0=50+j*20
				if m==0:
					fill(1,1,1)
					ellipse(x0-2,y0-4,5,5)
				else:
				 text( "%d" % m,'helvetica',16,x0,y0)	

run(MyScene())


