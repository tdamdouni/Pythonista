from visual import *
from random import *


print(uniform(2.2,4.4))

#ball1=sphere()

n=50
i=0
nn=[]
##while i<=n:
##    nn=nn+[i]
##    i=i+1
##print(nn)
##
##for b in nn:
##    print(b)
##print(nn[2])
balls=[]
m=1
while i<=n:
    balls=balls+[sphere(pos=(i,0,0), radius=.2, make_trail=True)]
    balls[i].p=vector(uniform(-2,2),uniform(4,14),0)*m    
    i=i+1

t=0
dt=0.01
g=vector(0,-9.8,0)

while t<3:
    rate(100)
    F=m*g
    for ball in balls:
        ball.p=ball.p+F*dt
        ball.pos=ball.pos +ball.p*dt/m
    t=t+dt
