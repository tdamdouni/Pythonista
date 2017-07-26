from visual import *
from visual.graph import *
#import pylab as pb
# the pylab module is used for making prettier graphs


###  These are the three curves for plotting
fun1=gcurve(color=color.cyan)
fun2=gcurve(color=color.red)
fun3=gcurve(color=color.yellow)

## the following two can be turned on if you want to use the pylab plot
#dis=display()
#dis.visible=false


## these are lists used to plot in pylab
#rx=[]
#bx=[]
#tp=[]




L=.16 # the length of a cart

#this draws a track.  You don't really need it
track=box(pos=vector(0,-.015,0), length=1.2, width=.1, height=.03,
          color=(.5,.5,.5), material=materials.chrome)

#This is the red cart
red=box(pos=vector(.5, 0.025, 0), length=L, width=.08, height=0.05,
        color=color.red, material=materials.plastic)


#the blue cart.  Isn't this obvious?
blue=box(pos=vector(0, 0.025, 0), length=L, width=.08, height=0.05,
        color=color.blue, material=materials.plastic)


t=0
dt=0.0001 #this is something you might want to play with changing.
red.m=.2535
blue.m=.2545
v0=.9738 #initial speed of launched cart
red.p=red.m*vector(-v0,0,0) #starting momentum of red
blue.p=vector(0,0,0) #starting momentum of blue

#This is the spring constant for the collision model
k=9000 #k needs to be set high, but you should try changing this

## A note about k.  In order to make non-elastic collisions, I have a
## differential spring constant.  I make the spring stiffer (higher k)
## while the two carts are moving towards each other and softwer (lower k)
## while moving away.  k0 is the starting spring constant
k0=k

## s is the length of the spring.  When the two carts are closer
## than this distance, the spring exerts a force.  You should try chaning
## this value
s=0.003
F=vector(0,0,0) #the starting force



#e = 1 means completely elastic collision
#e = 0 means completely inelasitic
#for e not equal to 1, I will change k for when the carts are moving away from
# each other.  for inelastic, if vb-vr = 0, then k=0
e=1.

## old_r is just used to tell if the two carts are moving towards or
## away from each other
old_r = red.pos.x-blue.pos.x-L

while blue.pos.x>-.6:
    rate(10000)

    # calc the distance between the carts
    r=red.pos.x-blue.pos.x-L

    # if they are close enough, turn on the force
    if red.pos.x-blue.pos.x<s+L:

        # if they are moving away, turn on the lower spring constant
        if abs(r)>abs(old_r):
            k=e*k
        else: k=k0

        #this calculates the actual spring force
        F=k*(r-s)*vector(1,0,0)
#        dt=0.001
    else:
        #if they aren't close enough, put the force back to zero
        F=vector(0,0,0)
#        dt=0.01

## Update momentum
    blue.p=blue.p+F*dt
    red.p=red.p-F*dt #notice this has a negative force.  Newton's 3rd law

## Update position
    blue.pos=blue.pos+blue.p*dt/blue.m
    red.pos=red.pos+red.p*dt/red.m
    old_r=r

## Update time    
    t=t+dt

## these are used for plotting in pylab
##    rx=rx+[red.pos.x]
##    bx=bx+[blue.pos.x]
##    tp=tp+[t]

## calculate the kinetic energy
    KEr=.5*mag(red.p)**2/red.m
    KEb=.5*mag(blue.p)**2/blue.m
    KET=KEr+KEb

## plotting.  You can plot position, momeutm or KE.  Whatever makes you
## happy.
    
    fun1.plot(pos=(t,red.p.x))
    fun2.plot(pos=(t,blue.p.x))
    fun3.plot(pos=(t,red.p.x+blue.p.x))


## this is stuff for printing in pylab
##print(123)
##pb.figure()
##pb.plot(tp,rx, linewidth=3, c='r')
##pb.plot(tp, bx, linewidth=3, c='b')
##pb.xlabel('Time [s]')
##pb.ylabel('Horizontal Position [m]')
##pb.grid(True)
###pb.show()
##pb.savefig('collision1.png')
    
    

