from __future__ import division
from visual import *
from random import *

# Kadir Haldenbilen, Feb. 2011

scene.width = 1024
scene.height = 800
scene.range = 3
scene.center = (-1.5,0,0)
scene.forward = (0.4,0,-1)
scene.title = "Medusa"

poly = shapes.circle() - shapes.circle(pos=(-0.5,0))
pc = poly.contour(0)
pc.append(pc[0])

tails = []
p0s = []
tpos = []
tfs = []
phis = []
sps = []
colors = [(1,0,0),(1,0,1),(0,0,1),(0,1,0),(1,1,0),(0,1,1),(1,1,1)]
nt = int(uniform(5,9))
ls = []
rt = 0.3

for tl in range(int(nt)):
    lt = uniform(2,4)
    dx = lt / 32.0
    tangle = tl*2*pi/nt
    p0 = (-0.1, rt*sin(tangle), rt*cos(tangle))
    sps.append(sphere(pos=p0, radius=0.05, color=(1,0,0)))
    t0s = []
    for i in range(32):
        t0s.append((p0[0]-i*dx, p0[1]- sin(pi-i*2*pi/32)*0.2,p0[2]))
    p0s.append(t0s)
    tfs.append(frame())
    c1 = int(uniform(0,7))
    c2 = int(uniform(0,7))
    c3 = int(uniform(0,7))
    c4 = int(uniform(0,7))
    phis.append(uniform(-pi/2,pi/2))
    ls.append(int(uniform(386,768)))
    tails.append(extrusion(frame=tfs[-1], pos=p0s[-1], shape=shapes.circle(radius=0.02),
                     color=[colors[c1],colors[c2],colors[c3],colors[c4]]*int(nt), material=materials.emissive))
    for i in range(len(tails[-1].scale)-2):
        tails[-1].scale[i] = uniform(0.8,1.2)
    tails[-1].scale[-2] = 0.3
    tails[-1].scale[-1] = 0.1

R = 0.01
dtheta = pi/20
arc = arange(0,2*pi+dtheta*2,dtheta)
    
E = extrusion(y=R*cos(arc), x=0, z=-R*sin(arc),  
          color=color.blue, shape=pc, material=materials.emissive)

ccr = shapes.rectangle(pos=(-0.3,0), width=0.2, height=0.01, rotate=-pi/6)
cfrm = frame()
collar = extrusion(pos=(0.2,0,0), y=0.5*cos(arc), x=0, z=-0.5*sin(arc), color=(0,0.2,0.8),
                   shape=ccr, material=materials.emissive, np=400, frame=cfrm)
scp = collar.pos.copy()

lc = len(collar.pos)
lt = len(tails)
t = 0.0
ts = nt*[0]
dlts = nt*[1]
pi2=pi*2
pi4=pi2*2
pi8=pi4*2
pi16 = pi8*2
pid2 = pi/2
pi28 = pi2*pi8
dlt = 1.0

while 1:
	ctpi8=cos(ts[0]/pi8)
	yxs = abs(1.0-ctpi8)*0.125
	E.yscale = 1.0+yxs
	E.xscale = 1.0-yxs
	collar.xscale = E.xscale
	collar.yscale = E.yscale
	for i in range(lc):
	    dt = sin(min(ts)+i*pi16/lc)*0.005
	    collar.pos[i][0] = scp[i][0]+dt
	    collar.pos[i][2] = scp[i][2]-dt
	for it in range(lt):
	    tail = tails[it]
	    lp = len(tail.pos)
	    tail.y = p0s[it][0][1] + sin(tail.x*ts[it]/(pi28)+phis[it])*tail.x*0.1
	    tail.frame.rotate(axis=tail.frame.axis, angle=ctpi8*0.005)
	    tail.frame.rotate(axis=(0,0,1), angle=ctpi8*0.00125)
	    tail.frame.x = ctpi8*0.05
	    ts[it] += dlts[it]
	    sps[it].pos = tail.frame.pos+tail.pos[0]
	    sps[it].color = (1,yxs*4,0)
	    if ts[it] >= ls[it]: dlts[it] = -1.0
	    if ts[it] <= 0: dlts[it] = +1.0
	E.color = (0,ctpi8*0.5,1)
	rate(25)
