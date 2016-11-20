from visual import *
from visual.graph import *

gra=gcurve(color=color.cyan)

dj=sphere(pos=(-2,0,0), radius=0.15, color=color.red)
dude=sphere(pos=(0,0,0), radius=0.1, color=color.cyan)

dj.m=100
dude.m=65
v=5.5
dj.p=vector(v,0,0)*dj.m
dude.p=vector(0,0,0)

k=100000 #spring constant for the interaction
sk=0.2 #the distance at which the spring starts to push

t=0
dt=0.001

while dude.pos.x<1.0:
    rate(1000)
    F=vector(0,0,0)
    if mag(dj.pos-dude.pos)<=sk:
        F=k*(sk-mag(dj.pos-dude.pos))*norm(dude.pos-dj.pos)
        dt=0.00001
    else:
        dt=0.001
    dj.p=dj.p-F*dt
    dude.p=dude.p+F*dt

    dj.pos=dj.pos+dj.p*dt/dj.m
    dude.pos=dude.pos+dude.p*dt/dude.m
    t=t+dt
    gra.plot(pos=(t,mag(F)))
