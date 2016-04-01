from visual import *
from visual.graph import *

fun1=gcurve(color=color.red)
fun2=gcurve(color=color.blue)
fun3=gcurve(color=color.yellow)

car1=box(pos=(-0.25, 0, 0), height=0.05, width=0.05, length=0.12, color=color.red)
car2=box(pos=(0.1, 0, 0), height=0.05, width=0.05, length=0.12, color=color.blue)

car1.m=0.1
car2.m=0.3

car1.p=car1.m*vector(0.4,0,0)
car2.p=car2.m*vector(0,0,0)

k=1.0e-4
t=0
dt=0.001



while car2.pos.x<0.5:
    rate(100)
    r=car2.pos-car1.pos
    F=k*norm(r)/mag(r)**3

    car1.p=car1.p+-F*dt
    car2.p=car2.p+F*dt
    car1.pos=car1.pos+car1.p*dt/car1.m
    car2.pos=car2.pos+car2.p*dt/car2.m
    t=t+dt
    fun1.plot(pos=(t,car1.p.x))
    fun2.plot(pos=(t,car2.p.x))
    fun3.plot(pos=(t,car2.p.x+car1.p.x))
