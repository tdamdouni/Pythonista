from visual import *
# Kadir Haldenbilen , Feb. 2011

scene.width = scene.height = 800
scene.forward = (0.2,-0.6,-0.8)
scene.title = "Differential Gear"

def scaler(start=(1.,1.), end=(1.,1.), np=2):
    sl = []
    for i in range(np):
        sl.append((start[0]+(end[0]-start[0])/(np-1)*i,
                   start[1]+(end[1]-start[1])/(np-1)*i))
    return sl
 
def bevelGears(R1=5.0, n1=15, t1=2.0, GR=2.0, hole1=False, hole2=False, twist=0.0):
    # Gear 2 radius and teeth numbers
    R2 = GR*R1
    n2 = int(GR*n1)

    # Calculate the thickness of gear 2, and the scaling factor
    r2 = R2-t1      # final radius of gear 2
    r1 = (R1/R2)*r2 # final radius of gear 1
    t2 = R1-r1      # thickness of gear 2
    scaling = r1/R1 # both extrusions are scaled by this factor

    g1 = shapes.gear(n=n1, radius=R1)
    if hole1: g1 -= shapes.circle(radius=R1/2.)
    g2 = shapes.gear(n=n2, radius=R2)
    if hole2: g2 -= shapes.circle(radius=R2/2.)

    lnp = 2
    if twist: lnp = 8  
    cfrm = frame()
    frm1 = frame()
    eg1 = extrusion(shape=g1, pos=paths.line(start=(0,0,0), end=(0,0,t1), np=lnp),
                   scale=scaler(start=(1,1),end=(scaling,scaling), np=lnp),
                    twist=-twist, frame=frm1)

    frm2 = frame(pos=(R1,0,R2), axis=(0,0,1))
    eg2 = extrusion(shape=g2, pos=paths.line(start=(0,0,0), end=(0,0,t2), np=lnp),
                   scale=scaler(start=(1,1),end=(scaling,scaling), np=lnp),
                    twist=twist/GR, frame=frm2, color=color.red)

    return R1, n1, R2, n2, eg1, eg2

R1 = 4.
n1 = 8
t1 = 3.
GR1 = 1.

R5 = 5.
n5 = 15
t5 = 4.
GR3 = 3.

R1, n1, R2, n2, eg1, eg2  = bevelGears(R1=R1, n1=n1, t1=t1, GR=GR1, twist=0.0)
R3, n1, R4, n2, eg3, eg4  = bevelGears(R1=R1, n1=n1, t1=t1, GR=GR1, twist=0.0)
R5, n5, R6, n6, eg5, eg6  = bevelGears(R1=R5, n1=n5, t1=t5, GR=GR3, hole2=True, twist=0.0)
eg5.color = (1,1,0)
eg6.color = (0,1,1)

f1 = eg1.frame
f2 = eg2.frame
f3 = eg3.frame
f4 = eg4.frame
f5 = eg5.frame
f6 = eg6.frame

f1.frame = eg6.frame
f1.rotate(axis=(0,1,0), angle=pi/2)
f1.pos = (-R3,0,R5)

f3.frame = eg6.frame
f3.rotate(axis=(0,1,0), angle=-pi/2)
f3.pos = (+R3,0,R5)

f2.frame = eg6.frame
f2.rotate(axis=(0,1,0), angle=-pi/2)
f2.pos = (0,0,R5+R1)

f4.frame = eg6.frame
f4.rotate(axis=(0,1,0), angle=pi/2)
f4.pos = (0,0,R5-R3)

f1.rotate(axis=(1,0,0), angle=pi/n1)
f3.rotate(axis=(1,0,0), angle=pi/n1)

p1 = box(frame=eg6.frame, pos=(R6/2,0,R5), size=(1,R5,R5*2),
         color=(0,0,1), opacity=0.5)
p2 = box(frame=eg6.frame, pos=(-R6/2.,0,R5), size=(1,R5,R5*2),
         color=(0,0,1), opacity=0.5)
shft = cylinder(frame=eg6.frame, pos=p1.pos, axis=p2.pos-p1.pos, radius=0.5,
                color=(0,1,0))
"""
dsk2 = extrusion(frame=eg2.frame, pos=[(0,0,0),(0,0,-0.5)],
               color=eg2.color[0], shape=(shapes.circle(radius=R2+0.4) -
                shapes.circle(radius=R2/2.)))
dsk4 = extrusion(frame=eg4.frame, pos=[(0,0,0),(0,0,-0.5)],
               color=eg4.color[0], shape=(shapes.circle(radius=R4+0.4) -
                shapes.circle(radius=R4/2.)))
dsk1 = extrusion(frame=eg1.frame, pos=[(0,0,0),(0,0,-0.5)],
               color=eg1.color[0], shape=(shapes.circle(radius=R1+0.4) -
                shapes.circle(radius=R1/2.)))
dsk3 = extrusion(frame=eg3.frame, pos=[(0,0,0),(0,0,-0.5)],
               color=eg3.color[0], shape=(shapes.circle(radius=R3+0.4) -
                shapes.circle(radius=R3/2.)))
dsk5 = extrusion(frame=eg5.frame, pos=[(0,0,0),(0,0,-0.5)],
               color=eg5.color[0], shape=(shapes.circle(radius=R5+0.4) -
                shapes.circle(radius=R5/2.)))
"""

dsk6 = extrusion(frame=eg6.frame, pos=[(0,0,0),(0,0,-0.5)],
               color=eg6.color[0], shape=(shapes.circle(radius=R6+0.4) -
                shapes.circle(radius=R6/2.)))

mshaft = extrusion(shape=shapes.ngon(np=8, radius=R5/2.), color=eg5.color[0]*0.5,
                   pos=[eg5.pos[0]+vector(0,0,1)*0.01, eg5.pos[0]-vector(0,0,1)*15], frame=eg5.frame)

raxis = extrusion(shape=shapes.ngon(np=8, radius=R2/4.), color=eg2.color[0]*0.5,
                   pos=[eg2.pos[0], eg2.pos[0]-vector(0,0,1)*15], frame=eg2.frame)
laxis = extrusion(shape=shapes.ngon(np=8, radius=R4/4.), color=eg4.color[0]*0.5,
                   pos=[eg4.pos[0], eg4.pos[0]-vector(0,0,1)*15], frame=eg4.frame)
rfl = box(pos=raxis.pos[-1], size=(0.2,10,5), color=(1,1,0), frame=eg2.frame)
lfl = box(pos=laxis.pos[-1], size=(0.2,10,5), color=(1,1,0), frame=eg4.frame)

sc = extrusion(shape=shapes.rectangle(width=R6+1, height=R5)-shapes.circle(radius=R2/3),
               pos=[(0,0,2*R5), (0,0,2*R5+1)], frame=eg6.frame, color=(0,0,1),
               material=materials.glass)


CC = curve(pos=[(-25,0,R6),(+25,0,R6)])                                    
run = False
ang = pi/200
ang2 = ang/(R6/R5)
strang = ang2/2.0
lbl = label(yoffset=300, line=0,
            text="            CLICK TO START OR PAUSE\nPRESS  R  OR  L  TO TURN, S FOR STRAIGHT")
key = "s"
while True:
    if scene.mouse.events:
        m = scene.mouse.getevent()
        if m.click == 'left':
            run = not run
    if scene.kb.keys:
        key = scene.kb.getkey()
        if key == "r" or key == "R":
            lbl.text = "TURNING RIGHT"
        if key == "l" or key == "L":
            lbl.text = "TURNING LEFT"
        if key == "s" or key == "S":
            lbl.text = "DRIVING STRAIGHT - PRESS  R  OR  L  TO TURN"
    if run:
        eg5.frame.rotate(axis=(0,0,1), angle=ang)
        eg6.frame.rotate(axis=(1,0,0), angle=ang2, origin=(0,0,R6))
        if key == "r" or key == "R":
            eg2.frame.rotate(axis=(0,0,1), angle=-strang, origin=f2.pos)
            eg4.frame.rotate(axis=(0,0,1), angle=+strang, origin=f4.pos)
            eg1.frame.rotate(axis=(1,0,0), angle=-strang, origin=f1.pos)
            eg3.frame.rotate(axis=(1,0,0), angle=+strang, origin=f3.pos)
        if key == "l" or key == "L":
            eg2.frame.rotate(axis=(0,0,1), angle=+strang, origin=f2.pos)
            eg4.frame.rotate(axis=(0,0,1), angle=-strang, origin=f4.pos)
            eg1.frame.rotate(axis=(1,0,0), angle=+strang, origin=f1.pos)
            eg3.frame.rotate(axis=(1,0,0), angle=-strang, origin=f3.pos)

    rate(100)
            
