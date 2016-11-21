from visual import *
from visual.graph import *

fun1=gcurve(color=color.yellow)
fun2=gcurve(color=color.white)


ground=box(pos=(0,0,0), length=.3, width=.3, height=0.01)
ball=sphere(pos=(0,0,0), radius=0.02, color=color.yellow,
            make_trail=True)
golf=sphere(pos=(0,0,0), radius=0.02, make_trail=True)
g= vector(0,-9.8,0)
ball.m=0.002
golf.m=0.045
rho=1.2
C=0.47
v0=10.
theta=30*pi/180.
ball.p=ball.m*vector(v0*cos(theta),v0*sin(theta),0)
golf.p=golf.m*vector(v0*cos(theta),v0*sin(theta),0)
A=pi*ball.radius**2
t=0
dt=0.001

while ball.pos.y>=0:
    rate(1000)
    F=ball.m*g-(.5*rho*A*C*mag(ball.p/ball.m)**2)*norm(ball.p)
    Fg=golf.m*g
    ball.p=ball.p+F*dt
    golf.p=golf.p+Fg*dt
    ball.pos=ball.pos+ball.p*dt/ball.m
    golf.pos=golf.pos+golf.p*dt/golf.m
    t=t+dt
    fun1.plot(pos=(t,ball.p.y/ball.m))
    fun2.plot(pos=(t,golf.p.y/golf.m))
