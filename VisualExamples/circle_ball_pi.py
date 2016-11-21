from visual import *


r=2.
ball=sphere(pos=(-r,0,0), radius=0.1, color=color.yellow, make_trail=True)
ball.v=vector(0,0.5,0)
start1=sphere(pos=ball.pos, radius=0.05, color=color.red)
t=0
dt=0.001
rt=ball.pos
a=-norm(ball.pos)*mag(ball.v)**2/r
ball.v=ball.v+a*dt
ball.pos=ball.pos+ball.v*dt
t=t+dt
start=vector(-r,0,0)
print(mag(ball.pos-start))
close=mag(ball.pos-start)
print(close)
run=True
while mag(ball.pos-start) >0.99*close:
    rate(1000)
    a=-norm(ball.pos)*mag(ball.v)**2/r
    ball.v=ball.v+a*dt
    ball.pos=ball.pos+ball.v*dt
    t=t+dt
print(ball.pos)
ds=mag(ball.pos-start1.pos)
print(ds)
print("pi = ")
C=mag(ball.v)*t+ds
print(C/(2*r))
