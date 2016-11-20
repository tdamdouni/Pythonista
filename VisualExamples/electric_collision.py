from visual import *
from visual.graph import *

f1=gcurve(color=color.cyan)
f2=gcurve(color=color.yellow)
f3=gcurve(color=color.red)
K=1

ball1=sphere(pos=(-3, 0,0), radius=.1, color=color.yellow, make_trail=True)
ball2=sphere(pos=(0,0,0), radius=.1, color=color.yellow, make_trail=True)

ball1.m=1
ball2.m=2.
ball1.p=ball1.m*vector(2.,.5,0)
ball2.p=vector(0,0,0)

t=0
dt=0.001

while ball2.pos.x<3.:
    rate(1000)
    r = ball2.pos-ball1.pos
    F1=-K*norm(r)/mag(r)**2
    ball1.p=ball1.p+F1*dt
    ball2.p=ball2.p-F1*dt
    ball1.pos=ball1.pos+ball1.p*dt/ball1.m
    ball2.pos=ball2.pos+ball2.p*dt/ball2.m
    t=t+dt
    f1.plot(pos=(t,mag(ball1.p)**2/(2*ball1.m)))
    f2.plot(pos=(t,mag(ball2.p)**2/(2*ball2.m)))
    f3.plot(pos=(t,mag(ball1.p)**2/(2*ball1.m)+mag(ball2.p)**2/(2*ball2.m)))
    
