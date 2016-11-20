from visual import *

t=0
dt=0.01
g=vector(0,-9.8,0)

ball = sphere(pos=(-1,1,0), radius=.15, color=color.cyan)
ball.v=vector(0.1,0,0)

floor=box(pos=(0,0,0), length=2, width=1, height=.1, color=color.blue)

while ball.pos.x<1:
    rate(100)
    ball.pos=ball.pos+ball.v*dt
    t=t+dt
