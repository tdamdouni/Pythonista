from visual import *
from visual.graph import *

fun1=gcurve(color=color.yellow)
fun2=gcurve(color=color.red)
fun3=gcurve(color=color.cyan)

alpha=sphere(pos=(-1,0.05,0), radius=0.05, color=color.red, make_trail=True)
gold=sphere(pos=(0,0,0), radius=0.05, color=color.yellow, make_trail=True)

gold.m=.2
alpha.m=0.05

gold.p=vector(0,0,0)
alpha.p=alpha.m*vector(1.,0,0)

q=1.
k=3.e-4

t=0
dt=0.01

while alpha.pos.x<1:
    rate(100)
    r=gold.pos-alpha.pos
    F=-k*q*q*norm(r)/mag(r)**2
    alpha.p=alpha.p+F*dt
    gold.p=gold.p-F*dt
    alpha.pos=alpha.pos+alpha.p*dt/alpha.m
    gold.pos=gold.pos+gold.p*dt/gold.m
    t=t+dt
    fun1.plot(pos=(t,gold.p.y))
    fun2.plot(pos=(t,alpha.p.y))
    fun3.plot(pos=(t,gold.p.y+alpha.p.y))

