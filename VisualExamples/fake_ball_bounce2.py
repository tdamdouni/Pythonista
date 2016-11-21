from visual import *

g=vector(0,-9.8,0)
h=1
ball=sphere(pos=(0,h,0), radius=0.05, material=materials.shiny)

ball.p=vector(0,-.0003,0)
ball.m=0.1
t=0
dt=0.001
floor = box(length=1, width=1, height=0.05, pos=vector(0,0,0), color=color.blue)
ball.v=vector(0,-4.5,0)
while True:
    
    while ball.pos.y>(floor.pos.y+ball.radius):
        rate(1000)
        ball.pos=ball.pos+ball.v*dt

    while ball.pos.y<h:
        rate(1000)
        ball.pos=ball.pos-ball.v*dt
        
        
    
    
