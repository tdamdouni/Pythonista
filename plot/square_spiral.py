from pylab import *

vx=0
vy=1

x=0
y=0

xp=[0]
yp=[0]

N=40
l=1 #length of the side
c=0 #step counter
s=0 #side counter
i=0
while i <N:
	x=x+vx
	y=y+vy
	c=c+1
	if c==l:
		s=s+1
		vt=vx
		vx=-vy
		vy=vt
		c=0
	if s==2:
		s=0
		l=l+1
	i=i+1
	xp=xp+[x]
	yp=yp+[y]
	
plot(xp,yp, linewidth=3)
show()

