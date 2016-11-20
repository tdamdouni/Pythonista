from visual import *
from visual.graph import *
fun1=gcurve(color=color.cyan)
v0=30
thetan=11*pi/180
theta=40*pi/180
ab=vector(1,3,-3.4)
print(ab)
g=vector(0,-9.8,0)
A=0.027
C=.35
m=.42
ball=sphere(pos=(0,0.01,0), radius=1., make_trail=True)
ball.m=m
ball.p=vector(v0*cos(theta)*cos(thetan),v0*sin(theta),0)*m
t=0
dt=0.01
alpha=50*pi/180
omega=vector(cos(alpha),sin(alpha),0)*2*pi/86400

ground=box(pos=(0,0,0), length=100, width=30, height=1, color=color.green)

curve(pos=[(0,0,0),(50,0,0)], radius=.7, color=color.red)
north=sphere(pos=(0,0,0), radius=0.7, color=color.cyan, make_trail= True)
north.v=100*vector(cos(thetan), 0, -sin(thetan))

rho=1.2
while ball.pos.y>0:
    rate(100)
    v=ball.p/m
    F=m*g-norm(v)*.5*rho*A*C*mag(v)**2-2*m*cross(omega,v)
    ball.p=ball.p+F*dt
    ball.pos=ball.pos+ball.p*dt/ball.m
    t=t+dt
    fun1.plot(pos=(ball.pos.x,ball.pos.z))
    

print(ball.pos)
