from visual import *
from visual.graph import *

fun1=gcurve(color=color.cyan)
fun2=gcurve(color=color.red)
fun3=gcurve(color=color.yellow)

ball=sphere(pos=(1,-2,3), radius=0.1, color=color.yellow, make_trail=True)

ball.v=vector(0,0,0)

t=0
dt=0.01

while True:
    rate(100)
    ball.a=vector(-3*ball.pos.x+2, -4*ball.pos.y, -2*ball.pos.z+1)
    ball.v=ball.v+ball.a*dt
    ball.pos=ball.pos+ball.v*dt
    
    t=t+dt
    fun1.plot(pos=(t,ball.pos.x))
    fun2.plot(pos=(t,ball.pos.y))
    fun3.plot(pos=(t,ball.pos.z))

print(ball.pos.x)
