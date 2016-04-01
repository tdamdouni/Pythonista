from visual import *

print("""
Drag or click to show the magnetic field interactively.
Mark the magnetic field vector at the end of the drag.
""")

scene.width = 600
scene.height = 600
Rbig = 0.6
L = 2*pi*Rbig
Rsmall = 0.2
k = 1E-7 # mu-zero/4pi
I = 1.0
Ncoils = 20
Bscale = (2.*Rsmall)/(4*pi*1E-7*Ncoils*I/L)

dphi = 2.*pi/Ncoils/50.
phi = arange(0,2*pi+dphi,dphi)
toroid=curve(x = Rbig*cos(phi)+Rsmall*cos(Ncoils*phi)*cos(phi),
            y = Rbig*sin(phi)+Rsmall*cos(Ncoils*phi)*sin(phi),
            z = -Rsmall*sin(Ncoils*phi))
toroid.color = (1,0.7,0.2)
toroid.radius = 0.01

delta = toroid.pos[1:] - toroid.pos[:-1]
center = (toroid.pos[:-1] + toroid.pos[1:])/2.
scene.range = 1.3*(Rbig+Rsmall)
vwidth = L/100

def BField(obs):
    r = obs-center
    rmag = mag(r)
    rmag.shape = (-1,1)
    try:  # numpy
        return (k*I*cross(delta, r)/rmag**3).sum(axis=0)
    except:  # old Numeric
        return sum(k*I*cross(delta, r)/rmag**3)

Bvector = arrow(axis=(0,0,0), shaftwidth=vwidth, color=(0,1,1))
drag = False

while True:
    rate(100)
    if drag:
        newobs = scene.mouse.pos
        if newobs != obs:
            obs = newobs
            Bvector.axis = Bscale*BField(obs)
            Bvector.pos = obs
    if scene.mouse.events:
        m = scene.mouse.getevent()
        if m.button == 'left':
            if m.press:
                obs = scene.mouse.pos
                Bvector.axis = Bscale*BField(obs)
                Bvector.pos = obs
            elif m.drag:
                drag = True
                obs = None # force update of position
    ##            scene.cursor.visible = 0 # not yet implemented
            elif m.release or m.drop:
                drag = False
    ##            scene.cursor.visible = 1 # not yet implemented
                arrow(pos=obs, axis=Bscale*BField(obs), shaftwidth=vwidth, color=(0,1,1))
                        
            


