from visual import *

stick=box(pos=(0,0,0), length=1, width=.2, height=.2, color=color.cyan)

w=.5

t=0
dt=0.01

while True:
    rate(100)
    stick.rotate(angle=w*dt, axis=(0,0,1), origin=stick.pos)
    t=t+dt
