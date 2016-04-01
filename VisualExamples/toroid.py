# Magnetic field of a toroid, using Biot-Savart law
# Ruth Chabay, Carnegie Mellon University, 2000-05-30

from visual import *

scene.width=800
scene.height=800
scene.title="Magnetic Field of a Toroid"
scene.minscale=.95

bigradius = 0.25
smallradius=0.03
I=1.
muthing=1e-7
nturns=75.  # number of loops in helix
nsteps=20.  # number of straight segments to approximate 1 turn
Bideal=muthing*2.*nturns*I/bigradius        # Ampere's law, inside helix
bscale = bigradius/(Bideal*4.)

# create toroid and arrows at observation locations
toroid = curve(color=(1.,.7,.2), radius=0.003)
tr = vector(bigradius, 0, 0)
dtheta=2*pi/(nsteps*nturns)
phi= 2*pi/nsteps
# use invisible arrows here because vector.rotate illegal at present
a=arrow(pos=(0,0,0), axis=tr, visible=0)
b=arrow(pos=a.axis, axis=(smallradius,0,0), visible=0)
zaxis=vector(0,0,1)
ocount=(nsteps*nturns/10.)  # in order to add zeroth observation loc
Barrows=[]

for t in arange(0, nsteps*nturns+1):
    a.rotate(angle=dtheta, axis=(0,0,1))
    b.rotate(angle=phi, axis=cross(zaxis,a.axis))
    toroid.append(pos=a.axis+b.axis)
    ocount=ocount+1
    if ocount > (nsteps*nturns/10.):
        ocount=0
        # outside toroid (note that B is *very* small here)
        c=arrow(pos=1.2*a.axis, axis=(0,0,0), color=(0,.6, 1), shaftwidth=0.005)
        # inside the wire helix (B proportional to 1/r)
        Barrows.append(c)
        c=arrow(pos=1.07*a.axis, axis=(0,0,0), color=(0,.6, 1), shaftwidth=0.005)
        Barrows.append(c)
        c=arrow(pos=a.axis, axis=(0,0,0), color=(0,.6, 1), shaftwidth=0.005)
        Barrows.append(c)
        c=arrow(pos=0.93*a.axis, axis=(0,0,0), color=(0,.6, 1), shaftwidth=0.005)
        Barrows.append(c)
        # inside toroid (small, in +z direction, due to loop current)
        c=arrow(pos=0.8*a.axis, axis=(0,0,0), color=(0,.6, 1), shaftwidth=0.005)
        Barrows.append(c)
        
# uncomment to visualize r
#rarrow=arrow(pos=(0,0,0), axis=(0,0,0), color=(1,0,1), shaftwidth=0.01)

# visualize dl as integration progresses
dlarrow=arrow(pos=(0,0,0), axis=(0,0,0), color=(0,1,0), shaftwidth=0.005)

oldpt = toroid.pos[0]
for pt in toroid.pos:
    dl=vector(pt-oldpt)
    source=oldpt+dl/2.
    dlarrow.axis=dl*2
    dlarrow.pos=source
    for b in Barrows:
        r=vector(b.pos-source)
# uncomment to visualize r
#        rarrow.pos=source
#        rarrow.axis=r
#        rate(30)
        dB=muthing*I*cross(dl,r)/r.mag**3
        b.axis=b.axis+dB*bscale
    oldpt=pt
dlarrow.visible=0
    
print("computed value at R: ",Barrows[2].axis.mag/bscale)
print("Ampere's law value: ", Bideal)
        
        
    
