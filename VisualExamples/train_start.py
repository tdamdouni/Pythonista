from visual import *
from visual.graph import *


## Setting up graphs for three of the cars
fun1=gcurve(color=color.cyan)
fun2=gcurve(color=color.yellow)
fun3=gcurve(color=color.red)
###

## this block is here so you can see the train move
block=box(pos=(0,-.15,0), length=.3, width=.1, height=0.05, color=color.cyan)

R=.1  ## the size of the spherical cars
L=.3    ##The spacing between cars


## you could try making the train engine mass different than the car mass
m=.1 ## mass of engine and cars

## dd is the amount that a car can move before getting a force.  This
## would be a good thing to try changing.
dd=0.01 

a=1.4  ## is a variable used to change the force a car experiences when a
        ## coupling is stretched
mut=.5  ## this is the coefficient of friction on the engine car
mucs=.1  ## this is the coefficient of static friction on a car
muck=0.09  ## coefficient of kinetic friction on a car
g=9.8   ##this is the gravitaional field - comes into play with fricitonal force

F=mut*m*9.8*vector(1,0,0) #this is the frictional force on the engine

##make the train engine (I call it the train)
train=sphere(pos=(0,0,0), radius=1.1*R, color=color.red)
train.m=m
train.p=vector(0,0,0)


## N is the number of cars
N=5
#cars is a list of spheres
cars=[]
#Fs is a list of forces on cars
Fs=[]
#r is the distance between cars
r=[]

## this loop goes through and adds cars to the list of cars
## it also sets the momentum, mass, and force 
for i in range(N):
    print(i)
    cars=cars+[sphere(pos=train.pos-vector((i+1)*L,0,0),radius=R)]
    cars[i].p=vector(0,0,0)
    cars[i].m=m
    Fs=Fs+[vector(0,0,0)]
    r=r+[L]

#add one final force for the end (it will always be zero)    
Fs=Fs+[vector(0,0,0)]

temp_start=cars[N-1].pos.x

t=0
dt=0.001

while cars[N-1].pos.x<(0.4+temp_start):
    rate(200) #rate sets how fast the program runs
    #I have to set the first distance manually
    r[0]=mag(train.pos-cars[0].pos)
    #reset the inter-car forces to zero
    for i in range(N):
        Fs[i]=vector(0,0,0)
    #calculate the inter-car distance
    for i in range(N-1):
        r[i+1]=mag(cars[i].pos-cars[i+1].pos)
    #recalculate the inter-car forces
    #these are the forces on the front of the car, not the rear
    for i in range(N):
        if r[i]>L+dd:
            Fs[i]=a*F
        if r[i]<L-dd:
            Fs[i]=-a*F
    ## update momentum for train engine
    train.p=train.p+(F-Fs[0])*dt


    ##update momentum for the cars
    for i in range(N):
        Ff=vector(0,0,0)
        #these two if statements determine the direction of the forces
        if mag(cars[i].p)>0:
            Ff=muck*cars[i].m*g*(-norm(cars[i].p))
        if mag(cars[i].p)==0:
            Ff=mucs*cars[i].m*g*(-norm(Fs[i]-Fs[i+1]))                                 
        cars[i].p=cars[i].p+(Fs[i]-Fs[i+1]+Ff)*dt

    ## update position of engine
    train.pos=train.pos+train.p*dt/train.m

    ## update position of the cars
    for i in range(N):
        cars[i].pos=cars[i].pos+cars[i].p*dt/cars[i].m
                

    t=t+dt

    ## these just make plots
    fun1.plot(pos=(t,train.pos.x))
    fun2.plot(pos=(t, cars[N-1].pos.x+N*L))
    fun3.plot(pos=(t, cars[2].pos.x+3*L))
