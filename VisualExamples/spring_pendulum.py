from visual import *
from visual.graph import *

fun1=gcurve(color=color.yellow)
fun2=gcurve(color=color.red)
g=vector(0,-9.8,0)
L=1.
t=0
dt=0.001

theta=40*pi/180.
omega=0

top=sphere(pos=(0,0,0), radius=0.05)
ball=sphere(pos=(L*sin(theta), -L*cos(theta),0), radius=.05, color=color.yellow,
            make_trail=True)
ball2=sphere(pos=(L*sin(theta), -L*cos(theta),0), radius=.1, color=color.red,
            make_trail=True)
ball2.m=.5
k=8000.
ball2.p=ball2.m*vector(0,0,0)

while True:
    rate(1000)
    alpha=g.y*theta/L
    omega=omega+alpha*dt
    theta=theta+omega*dt
    ball.pos=vector(L*sin(theta),-L*cos(theta),0)
    r=top.pos-ball2.pos
    F=ball2.m*g + k*(mag(r)-L)*norm(r)
    ball2.p=ball2.p+F*dt
    ball2.pos=ball2.pos+ball2.p*dt/ball2.m

    
    t=t+dt
    fun1.plot(pos=(t,theta))
    theta2=arctan(ball2.pos.x/(-ball2.pos.y))
    fun2.plot(pos=(t,theta2))
