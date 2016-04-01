from visual import *
# Kadir Haldenbilen, February 2011

print ("Click to pause or restart.")

scene.autocenter = True
scene.width = 1024
scene.height = 768

mfrm = frame(axis=(0,0,1))                  # Motor Frame
rfrm = frame(frame=mfrm)                    # Rotor Frame

# Create contactor
# First, draw the outer circle
g1 = shapes.circle(radius=1.2)
ns=24
# We will have 24 contactor surfaces, 2 per each rotor wiring
for i in range(ns):
    # Second, subtract rectangular pieces to get a slice for each contact surface
    t = shapes.rectangle(pos=(1.2*cos(i*2*pi/ns),1.2*sin(i*2*pi/ns)),
                         width=2.1, height=0.05, rotate=i*2*pi/ns)
    g1 = g1 - t

g1 = g1 - shapes.circle(radius=0.5)     # Last, subtract rotor shaft
cl = 2.0
# Now, extrude to get "cylindrical" contactor surfaces
ge1 = extrusion(pos=[(0,0,0),(0,0,cl)], shape=g1, color=(1,0.5,0.3),
                material=materials.rough, frame=rfrm)

# Create contactor soldering tips, same as above
g2 = shapes.circle(radius=1.4)
ns=24
sphs = []
for i in range(ns):
    t = shapes.rectangle(pos=(1.2*cos(i*2*pi/ns),1.2*sin(i*2*pi/ns)),
                         width=2.1, height=0.2, rotate=i*2*pi/ns)
    g2 = g2 - t
    sldr = sphere(frame=rfrm, pos=(1.195*cos(i*2*pi/ns+pi/ns),1.195*sin(i*2*pi/ns+pi/ns),2.2),
                  radius=0.1, material=materials.shiny)     # add solders
    sphs.append(sldr)

g2 = g2 - shapes.circle(radius=0.6)     # Subtract a wider circle to enable soldering

# Finally extrude to get soldering surfaces
ge2 = extrusion(pos=[(0,0,2),(0,0,2.4)], shape=g2, color=(1,0.5,0.3),
                material=materials.rough, frame=rfrm)

# Add shaft insulator material
# Define a circular ring of thickness=0.05
sc = shapes.circle(radius=0.5, thickness=0.05)
# Extrude the ring to get a thin hollow cylinder insulator over the shaft
sce = extrusion(pos=[(0,0,-0.5),(0,0,9.5)], shape=sc, color=(1,0,0),
                material=materials.plastic, frame=rfrm)

# The Rotor Shaft, defined by a simple cylinder
shaft = cylinder(frame=rfrm, pos=(0,0,-1.5), axis=(0,0,12), radius=0.495,
                 material=materials.blazed)
# Add a piece of gear at one end of the shaft
# Use the gear shape to define the shape, note radius, addendum, dedendum sizes
gr = shapes.gear(n=9, radius=0.455, addendum=0.04, dedendum=0.06, fradius=0.01)
# Extrude the gear shape appending it to the shaft end
gre = extrusion(frame=rfrm, pos=[(0,0,-1.5),(0,0,-3)], shape=gr,
                material=materials.blazed)

# Define Rotor Core
# Normally the core should have been built of many very thin sheets
# For performance reasons, a single block is built
# First define the outer circle
g3 = shapes.circle(radius=3.0)

ns=12
# We will have 12 wiring sections on the rotor core
for i in range(ns):
    # First define the vertical channels
    t1 = shapes.rectangle(pos=(3*cos(i*2*pi/ns),3*sin(i*2*pi/ns)),
                         width=1.1, height=0.3, rotate=i*2*pi/ns)
    # Then define winding hollow as a trapezoidal area
    t2 = shapes.trapezoid(pos=(2.*cos(i*2*pi/ns),2.*sin(i*2*pi/ns)),
                         width=1.2, top=0.5, height=1.4, roundness=0.1,
                          rotate=i*2*pi/ns+pi/2, )
    g3 = g3 - t2 - t1   # From the circle, subtract wiring areas

# Obtain rotor core profile
g3 = g3 - shapes.circle(radius=0.495)       # Subtract rotor shaft area

# Define rotor core body sizes
ps = 5.5
dlt = 0.05
thk = 5.04
nl = 1      # nl = 100
cf = frame(frame=rfrm, pos=(0,0, thk/2.+cl/2.0))
for i in range(nl):
    # Extrude rotor core profile to get the full core body
    ge3 = extrusion(pos=[(0,0,i*dlt),(0,0,i*dlt+thk)], shape=g3,
                    color=(0.7,0.7,0.705), twist=0.0, frame=cf)

# Do the core wire windings
# Here is a trick to build a saw-teeth profile, to represent many single windings
N = 20 # coils
vright = vector(.3,1.3)
r = mag(vright)/(2*N)
vright = norm(vright)
# S is the cross sectional profile of "winding block"
S = Polygon([(-.1,-.65), (0,-.65), (.3,.65), (-.1,.65)])
for n in range(N):
    right = vector(0,-.65)+(r+n*2*r)*vright
    # Add saw-teeth on the block to represent wires
    S += shapes.circle(pos=(right.x,right.y), radius=r, np=4)

# Define the winding path as a rounded rectangle
P = shapes.rectangle(width=.5, height=thk)
P += shapes.circle(pos=(0,-thk/2), radius=.25, np=10)
P += shapes.circle(pos=(0,+thk/2), radius=.25, np=10)
wrfs = []
for i in range(ns):
    # We need a separate frame for individiual winding section
    wrf = frame(frame=cf, pos=(0,2,thk/2.))
    wrfs.append(wrf)
    # Extrude the winding block per winding path
    wre = extrusion(frame=wrf, pos=P, shape=S,
                    color=(.7,.5,.15), material=materials.rough)
    # Make angular corrections to position on the rotor core
    wrf.rotate(axis=(0,0,1), angle=(i*2*pi/ns+pi/ns), origin=(0,0,0))

# Connect contactor surfaces to windings with cables
for i in range(ns):
    # Connect every other contactor to one end of windings (somewhere!)
    curve(frame=rfrm, pos=[sphs[i*2].pos, cf.pos+wrfs[i].pos], radius=0.05,
          color=(0.4,0.2,0))
    # Connect remaining ones to the other end of windings (somewhere!)
    curve(frame=rfrm, pos=[sphs[i*2+1].pos, cf.pos+wrfs[i].pos], radius=0.05,
        color=(0,0,1))

# Create Brushes
# From a rectangular cross section, subtract rotor contactor circle, leaving us two
# brushes on each sides of the contactor, with circular profile
br = shapes.rectangle(width=5, height=0.4) - shapes.circle(radius=1.21)
# Extrude the brush profile to get the brushes in 3D
bre = extrusion(frame=mfrm, pos=[(0,0,0.4),(0,0,1.6)], color=(0.1,0.1,0.15),
                material=materials.rough, shape=br)

# Create Brush Housings
# Define a rectangular frame, with a thickness of 0.1
bh = shapes.rectangle(width=1.3, height=0.5, thickness=0.1)
# Extrude the rectangular frame to obtain hollow boxes for each housing
bhe1 = extrusion(frame=mfrm, pos=[(1.4,0,1),(2.9,0,1)], shape=bh, color=(0.9,1,0.8),
                 material=materials.rough)
bhe2 = extrusion(frame=mfrm, pos=[(-1.4,0,1),(-2.9,0,1)], shape=bh, color=(0.9,1,0.8),
                 material=materials.rough)

# Place a screw on each housing to fix the power cables
# Create a screw head profile by subtracting a cross from a circle
scrh = shapes.circle(radius=1) - shapes.cross()
scrh.scale(0.15,0.15)
# Extrude a little to get the screw head
scrhw1 = extrusion(frame=mfrm, pos=[(2.7,0.2,1),(2.7,0.3,1)], shape=scrh, color=(1,1,0.8),
                 material=materials.rough)
scrhw2 = extrusion(frame=mfrm, pos=[(-2.7,0.2,1),(-2.7,0.3,1)], shape=scrh, color=(1,1,0.8),
                 material=materials.rough)

# Create the screw bodies
# Use a square to create the body with teeth
scrb = shapes.rectangle(scale=0.1)
# Extrude the square with twist parameter to get the teeth of the screw
scrbe1 = extrusion(frame=mfrm, pos=paths.line(start=(2.7,0.2,1), end=(2.7,-0.3,1),
                    np=20), shape=scrb, twist=0.4, color=(1,1,0.9),
                 material=materials.rough)
scrbe2 = extrusion(frame=mfrm, pos=paths.line(start=(-2.7,0.2,1), end=(-2.7,-0.3,1),
                    np=20), shape=scrb, twist=0.4, color=(1,1,0.9),
                 material=materials.rough)

# Place the brush system on a craddle
# Use a rectangular block, subtract rotor circle to allow space for the rotor
crdl = (shapes.rectangle(pos=(0,-0.9), width=5.8, height=1.4) -
        shapes.circle(radius=1.21) - shapes.circle(pos=(-2.2,-0.9), radius=0.1))
# Extrude the block to get the craddle
crdle = extrusion(frame=mfrm, pos=[(0,-0.05,0.2),(0,-0.05,1.8)],
                material=materials.plastic, shape=crdl)

# Connect power cables to the brushes
# Use simple curves to define cables
cbl1i = curve(frame=mfrm, pos=[scrhw1.pos[-2], scrhw1.pos[-2]- vector(-2,0,0)],
            radius=0.03, color=ge1.color)
cbl1o = curve(frame=mfrm, pos=[scrhw1.pos[-2], scrhw1.pos[-2]- vector(-1.5,0,0)],
            radius=0.05, color=(0,0,1))

cbl2i = curve(frame=mfrm, pos=[scrhw2.pos[-2], scrhw2.pos[-2]+ vector(-0.5,0,0)],
            radius=0.03, color=ge1.color)
cbl2i.append(pos=cbl2i.pos[-1]+(0,-2,0))
cbl2i.append(pos=cbl2i.pos[-1]+(7,0,0))
cbl2o = curve(frame=mfrm, pos=cbl2i.pos, radius=0.05, color=(1,0,0))
cbl2o.pos[-1]-= (0.5,0,0)

# Add ball-bearings at both ends of the shaft
# First create the cross section of the bearing
# From a rectangular shape subtract the circles for the balls, and then
# subtract another rectangle for the shaft
br = shapes.rectangle(width=0.54, height=0.75) - shapes.circle(radius=0.25) - shapes.rectangle(width=0.30,height=0.76)
b1f = frame(frame=rfrm, pos=(0,0,-0.75))
# Extrude the cross section along a full circle to get a ball bearing
br1 = extrusion(frame=b1f, pos=paths.circle(radius=0.75), shape=br,
                material=materials.blazed)
b1f.rotate(angle=pi/2)
b2f = frame(frame=rfrm, pos=(0,0,10.))
br2 = extrusion(frame=b2f, pos=paths.circle(radius=0.75), shape=br,
                material=materials.blazed)
b2f.rotate(angle=pi/2)

# Do not forget to add the balls
bbrs1 = []
bbrs2 = []
for i in range(7):
    bbrs1.append(sphere(frame=rfrm, pos=(0.75*cos(i*2*pi/7.0), 0.75*sin(i*2*pi/7.0), -0.75),
                        radius=0.25, material=materials.rough))
    bbrs2.append(sphere(frame=rfrm, pos=(0.75*cos(i*2*pi/7.0), 0.75*sin(i*2*pi/7.0), 10.),
                        radius=0.25, material=materials.rough))

# Define the stator core - again defined as a single block
# We did not include all stator parts here for better visualisation
# Use a rounded rectangle for the stator base.
# Subtract a large circle in the middle to allow for the rotor
# Subtract circular holes to place the stator windings
# Subtract some more holes for fixing the stator core on the motor body
stb = (shapes.rectangle(pos=(0,-2.25), width=6, height=3, roundness=0.5) -
       shapes.rectangle(width=8.5, height=4.6) - shapes.circle(radius=3.1) -
       shapes.circle(pos=(2.6,-2.1), radius=0.3) -
       shapes.circle(pos=(2.0,-3.4), radius=0.15) -
       shapes.circle(pos=(-2.6,-2.1), radius=0.3) -
       shapes.circle(pos=(-2.0,-3.4), radius=0.15))

# Extrude the stator profile to get the stator core
stbe = extrusion(frame=mfrm, pos=[(0,0,thk/2.+cl/2.0), (0,0,thk/2.+cl/2.0+thk)], shape=stb)


# Here is a complex path definition for stator winding, which is not planar.
# The path is made up of an arc in YZ + line in ZX + arc in ZY + line in XZ

tp = []
# Define the arc path
pp = shapes.arc(angle1=-pi/3.5, angle2=pi/3.5, radius=3.4)
cp = pp.contour(0)[0:len(pp.contour(0))//2]
for p in cp:
    tp.append((0,-p[0],p[1]))
# Create the reverse arc path
tmp = []
tmp.extend(tp)
tmp.reverse()
tp.append(vector(tp[-1])-vector(thk+0.7,0,0))
for p in tmp:
    # We are in 3D, not in 2D
    tp.append(vector(p)-vector(thk+0.7,0,0))
tp.append(vector(tp[-1])+vector(thk+0.7,0,0))
# Just a simple winding cross section for the whole of the stator winding
sts = shapes.circle(radius=0.3)
sfrm = frame(frame=mfrm, pos=(0,0,thk+cl*2-0.15))
# Extrude the winding profile along the complex stator path
stse = extrusion(frame=sfrm, pos=tp,
                 shape=sts, color=(1,0,0))
sfrm.rotate(axis=(0,1,0), angle=-pi/2)

# Create the motor cover as a rotational extrusion along the mootor
# Add two rounded rectangles which will cover all the rotor and stator.
# Leave the tips of shaft outside the cover
cvr = (shapes.rectangle(width=3, height=11.4, roundness=0.1) +
       shapes.rectangle(width=9, height=10, roundness=0.1))
cvrc = Polygon(cvr.contour(0))
# Create a scaled down copy of the same profile
cvrc.scale(0.95,0.95)
# Subtract the smaller one to get a thin "skin" to represent the cover
# We do not need the full profile, take out the lower half, allowing some
# space for the ball bearings
cvr = (cvr - cvrc -  shapes.rectangle(width=1.8, height=12) -
       shapes.rectangle(pos=(-4,0), width=7, height=12))
cfrm = frame(pos=(-4.6,0,0))
# Rotate the profile around the shaft along an arc to get the cover.
# Do not use full circle, so that we can see the inside of the motor
cvre = extrusion(frame=cfrm, pos=paths.arc(angle1=-pi/4, angle2=pi, radius=0.1),
                 shape=cvr, color=(0,0.6,0.3), material=materials.rough)
# Place the cover correctly
cfrm.rotate(angle=pi/2)
cfrm.rotate(axis=(0,1,0), angle=pi/2)
cfrm.rotate(axis=(1,0,0), angle=-pi/2)

# Connect power cables
angl = pi/400
run = True
# Turn on the motor
while True:
    rate(100)
    if run:
        rfrm.rotate(angle=angl, axis=(0,0,1))
    if scene.mouse.events:
        m = scene.mouse.getevent()
        if m.click == 'left':
            run = not run
            
