from __future__ import division
from visual import *
from visual.graph import *

fun1=gcurve(color=color.cyan)

def spring1(k,x0,v0,m):
    
 #   x0=.2
    ball=sphere(pos=(x0,0,0), radius=0.05)
#    ball.m=1
    ball.m=m
    ball.p=vector(v0,0,0)*ball.m
#    ball.p=vector(0,0,0)

    t=0
    dt=0.01

    while ball.pos.x<=x0:
        rate(1000000)
        F=-k*ball.pos
        ball.p=ball.p+F*dt
        ball.pos=ball.pos+ball.p*dt/ball.m
        t=t+dt
    return(t, ball.pos.x)

k=5.
dk=.5
while k<16.:
    fun1.plot(pos=(1/k,(spring1(k,.2, 0,1.)[0])**2))
    k=k+dk
print(spring1(k,.2, 0,1.))
print(spring1(k,.2, 0,1.)[0])
print(spring1(k,.2, 0,1.)[1])


