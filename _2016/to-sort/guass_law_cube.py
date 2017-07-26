from __future__ import division
from visual import *
#import pylab as pb


scene2=display(background=color.white)
#scene2.visible=False


L=1.
n=5 #how many pieces to break into (this would be nxn squares)
dL=L*1./n #square size



q=1e-9 #this is the charge
k=9e9  #1/4pie0 constant
ep0=1/(4*pi*9e9) #epislon 0 constant (for guass law)
charge=sphere(pos=(0,0,0), color=color.red, radius=L/20.) #not sure why I show this, you can't see it

# max flux is something you might need to change.  This is used to set the color of the squares
maxflux=abs((dL**2)*k*q/(L/2)**2)

flux=0
dflux=0


#####  this is the front face (+z)
#start with the center of one square
obs=vector(-L/2+dL/2, L/2-dL/2, L/2)

while obs.y>=(-L/2.+dL/2.):
    
    obs.x=-L/2+dL/2
    while obs.x<=L/2-dL/2:
        r=obs-charge.pos 
        E=k*q*norm(r)/mag(r)**2
        dflux = dot(E,vector(0,0,1))*dL**2
        if dflux>=0:
            box(pos=obs, length=dL, height=dL, width=dL/50, color=(dflux/maxflux,0,0),
                material=materials.emissive)
        if dflux <0:
            box(pos=obs, length=dL, height=dL, width=dL/50, color=(0,0,-dflux/maxflux),
                material=materials.emissive)
        flux=flux+dflux
        obs.x=obs.x+dL
    obs.y=obs.y-dL


### right face (+x)
obs=vector(L/2, L/2-dL/2, L/2-dL/2)

while obs.y>=(-L/2+dL/2):
    obs.z=L/2-dL/2
    while obs.z>=-L/2+dL/2:
        r=obs-charge.pos
        E=k*q*norm(r)/mag(r)**2
        dflux = dot(E,vector(1,0,0))*dL**2
        if dflux>=0:
            box(pos=obs, length=dL/50, height=dL, width=dL, color=(dflux/maxflux,0,0),
                material=materials.emissive)
        if dflux <0:
            box(pos=obs, length=dL/50, height=dL, width=dL, color=(0,0,-dflux/maxflux),
                material=materials.emissive)
        
        flux=flux+dflux
        obs.z=obs.z-dL
    obs.y=obs.y-dL

#### top face (+y)

obs=vector(-L/2+dL/2, L/2, L/2-dL/2)

while obs.x<=(L/2-dL/2):
    obs.z=L/2-dL/2
    while obs.z>=-L/2+dL/2:
        r=obs-charge.pos
        E=k*q*norm(r)/mag(r)**2
        dflux = dot(E,vector(0,1,0))*dL**2
        if dflux>=0:
            box(pos=obs, length=dL, height=dL/50, width=dL, color=(dflux/maxflux,0,0),
                material=materials.emissive)
        if dflux <0:
            box(pos=obs, length=dL, height=dL/50, width=dL, color=(0,0,-dflux/maxflux),
                material=materials.emissive)
        
        flux=flux+dflux
        obs.z=obs.z-dL
    obs.x=obs.x+dL

#####  this is the back face (-z)
obs=vector(-L/2+dL/2, L/2-dL/2, -L/2)

while obs.y>=-(L/2.-dL/2.):
    obs.x=-L/2+dL/2
    while obs.x<=L/2-dL/2:
        r=obs-charge.pos
        E=k*q*norm(r)/mag(r)**2
        dflux = dot(E,vector(0,0,-1))*dL**2
        if dflux>=0:
            box(pos=obs, length=dL, height=dL, width=dL/50, color=(dflux/maxflux,0,0),
                material=materials.emissive)
        if dflux <0:
            box(pos=obs, length=dL, height=dL, width=dL/50, color=(0,0,-dflux/maxflux),
                material=materials.emissive)
        flux=flux+dflux
        obs.x=obs.x+dL
    obs.y=obs.y-dL

### left face (-x)
obs=vector(-L/2, L/2-dL/2, L/2-dL/2)

while obs.y>=(-L/2+dL/2):
    obs.z=L/2-dL/2
    while obs.z>=-L/2+dL/2:
        r=obs-charge.pos
        E=k*q*norm(r)/mag(r)**2
        dflux = dot(E,vector(-1,0,0))*dL**2
        if dflux>=0:
            box(pos=obs, length=dL/50, height=dL, width=dL, color=(dflux/maxflux,0,0),
                material=materials.emissive)
        if dflux <0:
            box(pos=obs, length=dL/50, height=dL, width=dL, color=(0,0,-dflux/maxflux),
                material=materials.emissive)
        
        flux=flux+dflux
        obs.z=obs.z-dL
    obs.y=obs.y-dL


#### bottom face (-y)

obs=vector(-L/2+dL/2, -L/2, L/2-dL/2)

while obs.x<=(L/2-dL/2):
    obs.z=L/2-dL/2
    while obs.z>=-L/2+dL/2:
        r=obs-charge.pos
        E=k*q*norm(r)/mag(r)**2
        dflux = dot(E,vector(0,-1,0))*dL**2
        if dflux>=0:
            box(pos=obs, length=dL, height=dL/50, width=dL, color=(dflux/maxflux,0,0),
                material=materials.emissive)
        if dflux <0:
            box(pos=obs, length=dL, height=dL/50, width=dL, color=(0,0,-dflux/maxflux),
                material=materials.emissive)
        
        flux=flux+dflux
        obs.z=obs.z-dL
    obs.x=obs.x+dL

print(flux)
print(flux*ep0/q)

while True:
    rate(100)



