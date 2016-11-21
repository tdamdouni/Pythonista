from visual import *

Earth=sphere(pos=vector(0,0,0), radius =1, material=materials.earth)

R=2.75 #orbita radius in terms of radius of the planet
GM=1.47  #GM as determined from the game
v=sqrt(GM/R)  #starting speed for a circular orbit
rt=0.0338   #this is the acceleration due to the rocket

#sc is the spacecraft
sc=sphere(pos=(R,0,0), radius=0.1, make_trail=True)

#other is just an object with no thrust so you can see the difference
#thrust makes
other=sphere(pos=(R,0,0), radius=0.03, color=color.red, make_trail=True)

t=0
dt=.01
sc.m=1 #spacecraft mass of 1
sc.p=sc.m*vector(0,-v,0) #initial momentum
other.m=1
other.p=sc.p
Fr=vector(0,0,0)  #this is the rocket thrust force
scale=0.001  #it turns out I don't need this

#vt is an arrow to represent the rocket thrust.
vt=arrow(pos=sc.pos, axis=scale*Fr, color=color.yellow)

while t<30:
    rate(100)

    #here I turn on the thrust from t=5 to 10 sec
    if t>5. and t<10.:
        Fr=rt*norm(sc.p)
        scale=10
    else:
        Fr=vector(0,0,0)
        scale=0.001

    #Calculate the gravitational force plus rocket thrust (if any)
    F=-GM*norm(sc.pos)/mag(sc.pos)**2+Fr

    #update momentum
    sc.p=sc.p+F*dt

    #update position
    sc.pos=sc.pos+sc.p*dt/sc.m

    #update stuff for the other orbit
    other.p=other.p-GM*norm(other.pos)*dt/mag(other.pos)**2
    other.pos=other.pos+other.p*dt/other.m

    #update the thrust arrow
    vt.pos=sc.pos
    vt.axis=scale*Fr
    t=t+dt
