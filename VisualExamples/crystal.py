from visual import *
from random import random

# Bruce Sherwood; revised by Jonathan Brandmeyer
# Converted core calculations to numpy, Sept. 2010, Bruce Sherwood

N = 3
Ntotal = N*N*N
scolor = (1,0.5,0)
bcolor = (0,0.58,0.69)
springs = []
atoms = []
m = 1.
k = 1.
L = 1.
R = 0.3*L
Rs = 0.9*R # end of spring is Rs from center of atom

def getn(N, nx, ny, nz): 
    # find nth atom given nx, ny, nz
    return (ny)*(N**2)+(nx)*N+(nz)

def makespring(natom1, natom2, radius): 
    # make spring from nnth atom to iith atom
    if natom1 > natom2:
        r12 = atoms[natom2].pos-atoms[natom1].pos
        dir = norm(r12)
        springs.append( helix(pos=atoms[natom1].pos+Rs*dir,
            axis=(L-2*Rs)*dir,
            radius = radius, color=scolor, thickness = 0.04)) #, shininess=0.9))
        springs[-1].atom1 = atoms[natom1]
        springs[-1].atom2 = atoms[natom2]
        angle = springs[-1].axis.diff_angle( vector(0,1,0))
        # avoid pathologies if too near the y axis (default "up")
        if angle < 0.1 or angle > pi-0.1:
            springs[-1].up = vector(-1,0,0) 

def crystal(N=3, delta=1.0, R=None, sradius=None):
    if R == None:
        R = 0.2*delta
    if sradius == None:
        sradius = R/5.
    xmin = -(N-1.0)/2.
    ymin = xmin
    zmin = xmin
    natom = 0
    for ny in range(N):
        y = ymin+ny*delta
        hue = (ny)/(N+1.0)
        c = color.hsv_to_rgb((hue,1.0,1.0))
        for nx in range(N):
            x = xmin+nx*delta
            for nz in range(N):
                z = zmin+nz*delta
                atoms.append(sphere(pos=(x,y,z), radius=R, color=bcolor))
                atoms[-1].p = vector()
                atoms[-1].near = list(range(6))
                atoms[-1].wallpos = list(range(6))
                atoms[-1].natom = natom
                atoms[-1].indices = (nx,ny,nz)
                natom = natom+1
    for a in atoms:
        natom1 = a.natom
        nx, ny, nz = a.indices
        if nx == 0: # left
            # if this neighbor is the wall, save location:
            a.near[0] = None
            a.wallpos[0] = a.pos-vector(L,0,0)
        else:
            natom2 = getn(N,nx-1,ny,nz)
            a.near[0] = natom2
            makespring(natom1, natom2, sradius)
        if nx == N-1: # right
            a.near[1] = None
            a.wallpos[1] = a.pos+vector(L,0,0)
        else:
            natom2 = getn(N,nx+1,ny,nz)
            a.near[1] = natom2
            makespring(natom1, natom2, sradius)
            
        if ny == 0: # down
            a.near[2] = None
            a.wallpos[2] = a.pos-vector(0,L,0)
        else:
            natom2 = getn(N,nx,ny-1,nz)
            a.near[2] = natom2
            makespring(natom1, natom2, sradius)
        if ny == N-1: # up
            a.near[3] = None
            a.wallpos[3] = a.pos+vector(0,L,0)
        else:
            natom2 = getn(N,nx,ny+1,nz)
            a.near[3] = natom2
            makespring(natom1, natom2, sradius)
        
        if nz == 0: # back
            a.near[4] = None
            a.wallpos[4] = a.pos-vector(0,0,L)
        else:
            natom2 = getn(N,nx,ny,nz-1)
            a.near[4] = natom2
            makespring(natom1, natom2, sradius)
        if nz == N-1: # front
            a.near[5] = None
            a.wallpos[5] = a.pos+vector(0,0,L)
        else:
            natom2 = getn(N,nx,ny,nz+1)
            a.near[5] = natom2
            makespring(natom1, natom2, sradius)
        a.near = tuple(a.near)
        a.wallpos = tuple( a.wallpos)
        # Nearpos is a list of references to the nearest neighbors' positions,
        # taking into account wall effects.
        a.nearpos = []
        for i in range(6):
            natom = a.near[i]
            if natom == None: # if this nearest neighbor is the wall
                a.nearpos.append( a.wallpos[i])
            else:
                a.nearpos.append(atoms[natom].pos)
        
    return atoms

sradius = R/3.
vrange = 0.2*L*sqrt(k/m)
dt = 0.02*(2.*pi*sqrt(m/k))
scene.visible = False
atoms = crystal(N=N, delta=L, R=R, sradius=sradius)
scene.visible = True
scene.autoscale = False

ptotal = vector()
for a in atoms:
    px = m*(-vrange/2+vrange*random())
    py = m*(-vrange/2+vrange*random())
    pz = m*(-vrange/2+vrange*random())
    a.p = vector(px,py,pz)
    ptotal = ptotal+a.p

for a in atoms:
    a.p = array(a.p-ptotal/(N**2))

# Convert to tuples for faster indexing access.  We aren't growing any more of them.
springs = tuple(springs)
atoms = tuple(atoms)

# Evaluate a couple of constants outside the loop
k_dt = k * dt
dt_m = dt / m

while True:
    rate(100)
    for a in atoms:
        r = array(a.nearpos) - a.pos
        rmag = (sqrt(sum(square(r),-1))).reshape(-1,1) # reshape rmag from row to column
        a.p += k_dt * sum((1-L/rmag)*r,0) # sum the forces k*dt*(rmag-L)*(r/rmag)

    for a in atoms:
        a.pos += a.p * dt_m

    for s in springs:
        p1 = s.atom1.pos
        r12 = s.atom2.pos-p1
        direction = r12.norm()
        s.pos = p1+Rs*direction
        s.axis = (r12.mag-2*Rs)*direction

