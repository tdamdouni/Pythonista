from visual import *
from time import clock
from random import random

# Stars interacting gravitationally
# Program uses numpy arrays for high speed computations

win=600

Nstars = 20  # change this to have more or fewer stars

G = 6.7e-11 # Universal gravitational constant

# Typical values
Msun = 2E30
Rsun = 2E9
L = 4e10
vsun = 0.8*sqrt(G*Msun/Rsun)

scene = display(title="Stars", width=win, height=win,
                range=2*L, forward=(-1,-1,-1))

xaxis = curve(pos=[(0,0,0), (L,0,0)], color=(0.5,0.5,0.5))
yaxis = curve(pos=[(0,0,0), (0,L,0)], color=(0.5,0.5,0.5))
zaxis = curve(pos=[(0,0,0), (0,0,L)], color=(0.5,0.5,0.5))

Stars = []
colors = [color.red, color.green, color.blue,
          color.yellow, color.cyan, color.magenta]
poslist = []
plist = []
mlist = []
rlist = []

for i in range(Nstars):
    x = -L+2*L*random()
    y = -L+2*L*random()
    z = -L+2*L*random()
    r = Rsun/2+Rsun*random()
    Stars = Stars+[sphere(pos=(x,y,z), radius=r, color=colors[i % 6],
                   make_trail=True, interval=10)]
    mass = Msun*r**3/Rsun**3
    px = mass*(-vsun+2*vsun*random())
    py = mass*(-vsun+2*vsun*random())
    pz = mass*(-vsun+2*vsun*random())
    poslist.append((x,y,z))
    plist.append((px,py,pz))
    mlist.append(mass)
    rlist.append(r)

pos = array(poslist)
p = array(plist)
m = array(mlist)
m.shape = (Nstars,1) # Numeric Python: (1 by Nstars) vs. (Nstars by 1)
radius = array(rlist)

vcm = sum(p)/sum(m) # velocity of center of mass
p = p-m*vcm # make total initial momentum equal zero

dt = 1000.0
Nsteps = 0
pos = pos+(p/m)*(dt/2.) # initial half-step
time = clock()
Nhits = 0

while True:
    rate(100)
    
    # Compute all forces on all stars
    r = pos-pos[:,newaxis] # all pairs of star-to-star vectors
    for n in range(Nstars):
        r[n,n] = 1e6  # otherwise the self-forces are infinite
    rmag = sqrt(sum(square(r),-1)) # star-to-star scalar distances
    hit = less_equal(rmag,radius+radius[:,newaxis])-identity(Nstars)
    hitlist = sort(nonzero(hit.flat)[0]).tolist() # 1,2 encoded as 1*Nstars+2
    F = G*m*m[:,newaxis]*r/rmag[:,:,newaxis]**3 # all force pairs
        
    for n in range(Nstars):
        F[n,n] = 0  # no self-forces
    p = p+sum(F,1)*dt

    # Having updated all momenta, now update all positions         
    pos = pos+(p/m)*dt

    # Update positions of display objects; add trail
    for i in range(Nstars):
        Stars[i].pos = pos[i]

    # If any collisions took place, merge those stars
    for ij in hitlist:
        i, j = divmod(ij,Nstars) # decode star pair
        if not Stars[i].visible: continue
        if not Stars[j].visible: continue
        # m[i] is a one-element list, e.g. [6e30]
        # m[i,0] is an ordinary number, e.g. 6e30
        newpos = (pos[i]*m[i,0]+pos[j]*m[j,0])/(m[i,0]+m[j,0])
        newmass = m[i,0]+m[j,0]
        newp = p[i]+p[j]
        newradius = Rsun*((newmass/Msun)**(1./3.))
        iset, jset = i, j
        if radius[j] > radius[i]:
            iset, jset = j, i
        Stars[iset].radius = newradius
        m[iset,0] = newmass
        pos[iset] = newpos
        p[iset] = newp
        Stars[jset].trail_object.visible = False
        Stars[jset].visible = 0
        p[jset] = vector(0,0,0)
        m[jset,0] = Msun*1E-30  # give it a tiny mass
        Nhits = Nhits+1
        pos[jset] = (10.*L*Nhits, 0, 0) # put it far away

    Nsteps += 1
