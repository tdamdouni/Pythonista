from visual import *
# Kadir Haldenbilen, March 2011

scene.width = 1024
scene.height = 768
scene.title = "Extrusion Quick-Tutorial"
scene.forward = (0,-.3,-1)

def pause():
    while True:
        rate(50)
        if scene.mouse.events:
            m = scene.mouse.getevent()
            if m.click == 'left': return
        elif scene.kb.keys:
            k = scene.kb.getkey()
            return

lbl = label(yoffset=300, text="CLICK OR PRESS A KEY TO ADVANCE\n\nIt is useful to rotate the displays you'll see", line=0)
et = extrusion(pos=[(0,0,0.5),(0,0,0.0)], shape="ref plane", color=color.blue)
rp = box(size=(4,3,0.01),opacity=0.5, color=color.white)
pause()
lbl.text = "ref plane is our reference plane\nto better visualize the position and the scale of\nthe following objects in this tutorial"

pause()
rp.visible=0
del(rp)
lbl.text = "r = shapes.rectangle(width=5, height=3), and\nre = extrusion(shape=r)\ntogether define a 2D rectangle of size 5x3 on XY plane"
r = shapes.rectangle(width=5, height=3)
re = extrusion(shape=r)         # Defines a 2D rectangle of size (5x3)
pause()
re.visible = 0
del(re)

lbl.text = "re = extrusion(pos=paths.line(), shape=r)\n\ndefines a rectangular box of size 5x3 with thickness=1"
re = extrusion(pos=paths.line(), shape=r)
pause()
re.visible = 0
del(re)
lbl.text = "re = extrusion(pos=paths.line(end=(0,0,-3)), shape=r)\n\ndefines a rectangular box of size 5x3 with thickness=3"

re = extrusion(pos=paths.line(end=(0,0,-3)), shape=r)
pause()
re.visible = 0
del(re)
lbl.text = "re = extrusion(pos=paths.rectangle(width=15, height=10), shape=r)\n\ndefines a rectangular box extruded along a rectangular path of 15x10 on XZ plane"

re = extrusion(pos=paths.rectangle(width=15, height=10), shape=r)   # Defines a
# rectangular box of thickness 3, extruded along a rectangular path of (15x10),
#which looks like a thick frame on XZ plane.
pause()
re.visible = 0
del(re)
lbl.text = "re = extrusion(pos=paths.circle(radius=10), shape=r)\n\ndefines a rectangular box extruded along a circular path of radius=10 on XZ plane"

re = extrusion(pos=paths.circle(radius=10), shape=r)   # Defines a ring with a
# radius=10 and rectangular cross section of size (5x3)
pause()
re.visible = 0
del(re)
lbl.text = "re = extrusion(pos=paths.arc(angle1=0, angle2=pi, radius=10), shape=r)\n\ndefines an arc of radius=10 and length=pi with a rectangular cross section of 5x3 on XZ plane"

re = extrusion(pos=paths.arc(angle1=0, angle2=pi, radius=10), shape=r) # Defines
# an arc of radius=10 and length pi with a rectangular cross section of size (5x3)
pause()
re.visible = 0
del(re)
lbl.text = "re = extrusion(pos=paths.arc(angle1=0, angle2=pi, radius=10, np=200), shape=r, twist=0.02)\n\nadds some twist on the same arc. Note np increased to 200 for better resolution"

re =extrusion(pos=paths.arc(angle1=0, angle2=pi, radius=10, np=200), shape=r,
               twist=0.02) # Defines the same arc with some twisting applied
# along the path
pause()
re.visible = 0
del(re)
lbl.text = "r = shapes.rectangle(width=5, height=3) - shapes.rectangle(width=4, height=2)\nre = extrusion(shape=r)\ntogether define a rectangle with a rectangular hole"

r = shapes.rectangle(width=5, height=3) - shapes.rectangle(width=4, height=2)
# Defines a rectangle with arectangular hole

re = extrusion(shape=r)         # Defines a 2D rectangle of size (5x3)
pause()
re.visible = 0
del(re)
lbl.text = "r = shapes.rectangle(width=5, height=3) - shapes.rectangle(width=4, height=2)\nre = extrusion(pos=paths.line(), shape=r)\ntogether define a rectangular hollow box of thickness=1"

re = extrusion(pos=paths.line(), shape=r)   # Defines a rectangular hollow
                                            # rounded box of thickness 1
pause()
re.visible = 0
del(re)
lbl.text = "r = shapes.rectangle(width=5, height=3) - shapes.rectangle(width=4, height=2)\nre = extrusion(pos=paths.line(end=(0,0,-3)), shape=r)\ntogether define a rectangular hollow box of thickness=3"

re = extrusion(pos=paths.line(end=(0,0,-3)), shape=r)   # Defines a rectangular 
                                                        # hollow box of thickness 3
pause()
re.visible = 0
del(re)
lbl.text = "r = shapes.rectangle(width=5, height=3) - shapes.rectangle(width=4, height=2)\nre = extrusion(pos=paths.arc(angle1=0, angle2=pi, radius=10), shape=r)\nextrudes the hollow box along the arc of length pi"

re = extrusion(pos=paths.arc(angle1=0, angle2=pi), shape=r, radius=10) # Defines
# an arc of radius=10 and length pi with a hollow rectangular cross section of size (5x3)
pause()
re.visible = 0
del(re)
lbl.text = "r = shapes.rectangle(width=5, height=3) - shapes.rectangle(width=4, height=2)\nre = extrusion(pos=paths.arc(angle1=0, angle2=pi, radius=10, np=200), shape=r, twist=0.02)\ntwists the arc along its length"

re = extrusion(pos=paths.arc(angle1=0, angle2=pi, radius=10, np=200), shape=r,
               twist=0.02) # Defines the same arc with some twisting applied
pause()
re.visible = 0
del(re)
lbl.text = "Let's re-build The Pentagon\nr = shapes.pentagon() - shapes.rectangle(width=0.7)\nre = extrusion(pos=paths.pentagon(), end=-2), shape=r)"

re = extrusion(pos=paths.pentagon(), shape=shapes.pentagon() - shapes.rectangle(width=0.7))
re.end = -2
pause()
re.visible = 0
del(re)
lbl.text = "We can have a rounded rectangle like this\n\nr = shapes.rectangle(width=5, height=3, roundness=0.1)"
r = shapes.rectangle(width=5, height=3, roundness=0.1)
re = extrusion(shape=r)         # Defines a 2D rectangle of size (5x3)
pause()
re.visible = 0
del(re)
lbl.text = ".. and a rounded box like this\n\nr = shapes.rectangle(width=5, height=3, roundness=0.1)"
r = shapes.rectangle(width=5, height=3, roundness=0.1)
re = extrusion(pos=paths.line(end=(0,0,-3)), shape=r)         # Defines a 2D rectangle of size (5x3)
pause()
re.visible = 0
del(re)
lbl.text = ".. or an inverse rounded box (chamfer) like this\n\nr = shapes.rectangle(width=5, height=3, roundness=0.1, invert=True)"
r = shapes.rectangle(width=5, height=3, roundness=0.1, invert=True)
re = extrusion(pos=paths.line(end=(0,0,-3)), shape=r)         # Defines a 2D rectangle of size (5x3)
pause()
re.visible = 0
del(re)
lbl.text = "We can have a rectangular frame like this\n\nr = shapes.rectangle(width=5, height=3, thickness=0.1)"
r = shapes.rectangle(width=5, height=3, thickness=0.1)
re = extrusion(shape=r)         # Defines a 2D rectangle of size (5x3)
pause()
re.visible = 0
del(re)
lbl.text = "...or a rounded rectangular frame like this\n\nr = shapes.rectangle(width=5, height=3, thickness=0.1, roundness=0.1)"
r = shapes.rectangle(width=5, height=3, thickness=0.1, roundness=0.1)
re = extrusion(shape=r)         # Defines a 2D rectangle of size (5x3)
pause()
re.visible = 0
del(re)
lbl.text = "...or an inverse rounded rectangular frame like this\n\nr = shapes.rectangle(width=5, height=3, thickness=0.1, roundness=0.1, invert=True)"
r = shapes.rectangle(width=5, height=3, thickness=0.1, roundness=0.1, invert=True)
re = extrusion(shape=r)         # Defines a 2D rectangle of size (5x3)
pause()
re.visible = 0
del(re)
lbl.text = "There are plenty of ready shapes in the library"
r = shapes.rectangle(pos=(0,0))
re = extrusion(shape=r)         # Defines a 2D rectangle of size (5x3)
c = shapes.circle(pos=(0,2))
re = extrusion(shape=c)
t = shapes.triangle(pos=(0,-2))
re = extrusion(shape=t)
e = shapes.ellipse(pos=(2,2))
re = extrusion(shape=e)
p = shapes.trapezoid(pos=(-2,2))
re = extrusion(shape=p)
h = shapes.hexagon(pos=(2,-2))
re = extrusion(shape=h)
s = shapes.star(pos=(-2,0))
re = extrusion(shape=s)
g = shapes.pentagon(pos=(2,0))
re = extrusion(shape=g)
n = shapes.ngon(np=7, pos=(-2,-2))
re = extrusion(shape=n)
rt = extrusion(pos=[(-2,-2,0.1),(-2,-2,0)], color=(1,0,0), shape="ngon", scale=0.5)

pause()
re.visible = 0
del(re)

for i in range(2,len(scene.objects)):
    o = scene.objects[2]
    o.visible = 0
    del(o)
lbl.text = "We can use scaling parameter to obtain a scaled cross section\nat the end or along the extrusion object:\nre = extrusion(pos=[(0,0,0),(0,0,-2)], shape=r, scale=[(0.5,0.5),(1,1)])"
r = shapes.rectangle(width=5, height=3)
re = extrusion(pos=[(0,0,0),(0,0,-2)], shape=r, scale=[(0.5,0.5),(1,1)])
st = extrusion(shape="Sample Extrusion Objects", visible=False)
pause()
re.visible = 0
del(re)
lbl.visible = 0
et.visible = 0
del(et)
st.visible = True
pause()

lbl.text = "SIMPLE COLUMN"
lbl.visible = 1
st.visible = 0
del(st)
pause()
lbl.text = "First Let's get a base\n\nee = extrusion(pos=[(-1,-1.5,0), (-1,-1.2,0)], shape=shapes.rectangle(width=0.40, roundness=0.1, invert=True))"
ee = extrusion(shape=shapes.rectangle(width=0.40, roundness=0.1, invert=True),
               pos=[(-1,-1.5,0), (-1,-1.2,0)])
pause()
lbl.text = "... add a column here\n\nee = extrusion(pos=[(-1,-1.2,0),(-1,0.5,0)], shape=shapes.ngon(np=16, radius=0.20), scale=[(1,1),(0.75,0.75)])"
ee = extrusion(pos=[(-1,-1.2,0),(-1,0.5,0)], shape=shapes.ngon(np=16, radius=0.20),
               scale=[(1,1),(0.75,0.75)])
pause()
lbl.text = "Next for the other side\n\nee = extrusion(pos=[(+1,-1.5,0), (+1,-1.2,0)], shape=shapes.rectangle(width=0.40, roundness=0.1, invert=True))"
ee = extrusion(pos=[(+1,-1.5,0), (+1,-1.2,0)],
               shape=shapes.rectangle(width=0.40, roundness=0.1, invert=True))
pause()
lbl.text = "... another column here\n\nee = extrusion(pos=[(+1,-1.2,0),(+1,0.5,0)], shape=shapes.ngon(np=16, radius=0.20), scale=[(1,1),(0.75,0.75)])"
ee = extrusion(pos=[(+1,-1.2,0),(+1,0.5,0)], shape=shapes.ngon(np=16, radius=0.20),
               scale=[(1,1),(0.75,0.75)])
pause()
lbl.text = "Now we need an arc on top\n\nee = extrusion(frame=afrm, pos=paths.arc(radius=1, angle1=0, angle2=pi, shape=shapes.circle(radius=0.15)))"
afrm = frame(pos=(0,0.5,0))
ee = extrusion(pos=paths.arc(radius=1, angle1=0, angle2=pi), shape=shapes.circle(radius=0.15),
               frame=afrm)
pause()
lbl.text = "Oops, we need to flip the arc"
afrm.rotate(angle=pi/2)
pause()
for i in range(1,len(scene.objects)):
    try:
        o = scene.objects[1]
        o.visible = 0
        del(o)
    except: continue
lbl.text = "BALL BEARING"
pause()
scene.range = 4
lbl.text = "Let's start with a simple rectangle (actually, a square)\n\nr = shapes.rectangle(width=1.5)"
r = shapes.rectangle(width=1.5)
re = extrusion(shape=r)
pause()
re.visible=0
del(re)
lbl.text = "and subtract a circle from it\n\nrc = shapes.rectangle(width=1.5) - shapes.circle(radius=0.5)"
rc = r - shapes.circle(radius=0.5)
re = extrusion(shape=rc)
pause()
re.visible=0
del(re)
lbl.text = "and subtract another piece of rectangle from it\n\nrcr = shapes.rectangle(width=1.5) - shapes.circle(radius=0.5) - shapes.rectangle(width=0.75, height=2)"
r2 = shapes.rectangle(width=0.75, height=2)
rcr = rc - r2
re = extrusion(shape=rcr)
pause()
re.visible=0
del(re)
lbl.text = "Now, let's extrude this object along a circle around the y-axis with the radius of the shaft\n\nre = extrusion(pos=paths.circle(radius=1.5), shape=rcr)"
ya = curve(pos=[(0,-3,0),(0,3,0)])
bb1 = frame()
re = extrusion(frame=bb1, pos=paths.circle(radius=1.5), shape=rcr)
for i in range(len(re.pos)):
    re.end = i
    rate(8)
pause()
lbl.text = "Let's add the balls"
bs = []
for i in range(7):
    bs.append(sphere(radius=0.5, pos=(1.5*sin(i*2*pi/7),0,1.5*cos(i*2*pi/7)), frame=bb1))
pause()
lbl.text = "... and finish with some materials"
re.material = materials.blazed
for b in bs:
    b.material = materials.rough
pause()
lbl.text = "Let's put this ball-bearing here like this"
scene.range = 12
bb1.rotate(axis=(0,0,1), angle=pi/2)
bb1.pos = (7,0,0)
pause()
lbl.text = "... and add another one there"
bb2 = frame()
re2 = extrusion(frame=bb2, pos=paths.circle(radius=1.5), shape=rcr)
re2.material = materials.blazed
bs2 = []
for i in range(7):
    bs2.append(sphere(radius=0.5, pos=(1.5*sin(i*2*pi/7),0,1.5*cos(i*2*pi/7)), frame=bb2))
for b in bs2:
    b.material = materials.rough
bb2.rotate(axis=(0,0,1), angle=pi/2)
bb2.pos = (-7,0,0)
ya.visible = 0
del(ya)
pause()
lbl.text = "Let's add a shaft through these bearings\n\nIt is a normal cylinder object"
shft = cylinder(pos=(0,+1.5,0), axis=(0,-18.5,0), radius=0.75, material=materials.blazed, frame=bb2)
pause()
lbl.text = "Let's assume this is the rotor"
rtr1 = cylinder(pos=(0,-1.5,0), axis=(0,-9.,0), radius=4, color=(0.7,0.7,0.71), material=materials.rough, frame=bb2)
rtr2 = cylinder(pos=(0,-1.0,0), axis=(0,-12.,0), radius=1.0, color=(1,0.8,0), material=materials.rough, frame=bb2)
pause()
lbl.text = "Now, let's build a cover for this electric motor, \nallowing some additional space for the stator also"
pause()
lbl.text = "We start with a rectangle\n\nr1 = shapes.rectangle(width=12., height=12, roundness=0.1)"
r1 = shapes.rectangle(width=12., height=12, roundness=0.1)
cr1 = extrusion(shape=r1)
pause()
lbl.text = "... and add another rectangle\nr2 = shapes.rectangle(width=15.5, height=5, roundness=0.1)\ncr = r1+r2"
r2 = shapes.rectangle(width=15.5, height=5, roundness=0.1)
cr2 = extrusion(shape=r2)
cr = r1+r2
pause()
lbl.text = "We make a scaled down copy of the total profile\ncrc = Polygon(cr.contour(0))\ncrc.scale(0.95,0.915)"
crc = Polygon(cr.contour(0))
crc.scale(0.95,0.915)
cr3 = extrusion(pos=[(0,0,0),(0,0,0.1)], shape=(crc), color=(0,0,1))
pause()
lbl.text = "and then subtrcat it from the first"
crs = cr-crc
csc = extrusion(shape=crs, color=(1,1,0))
cr1.visible=0
cr2.visible=0
cr3.visible=0
del(cr1)
del(cr2)
del(cr3)
pause()
lbl.text = "Now, cut out the lower half of this profile, \nby subtracting another rectangle from it\ncrh = crs - shapes.rectangle(pos=(0,-6), width=16, height=12)"
crh = crs - shapes.rectangle(pos=(0,-6), width=16, height=12)
csc.visible=0
del(csc)
cre = extrusion(shape=crh, color=(1,0,0))
pause()
lbl.text = "Also subtract another rectangle, \nto allow housing for the bearings\nrb = shapes.rectangle(width=16, height=4.5)"
rb = shapes.rectangle(width=16, height=4.5)
crh = crh - rb
cre.visible=0
del(cre)
cf=frame()
cre = extrusion(shape=crh, color=(1,0,0))
pause()
pos=array(paths.arc(angle1=-pi/2, angle2=+1.5*pi, radius=4.1).pos)
crh.rotate(-pi/2)
lbl.text = "Now we can extrude the final shape to get the motor cover\nby rotating the profile along a circle\nmh = extrusion(pos=paths.arc(angle1=-pi/2, angle2=+1.5*pi, radius=4.1), shape=crh, color=(0,1,0), material=materials.rough, frame=mf)"
mf = frame()
mh = extrusion(frame=mf, pos=pos, shape=crh, color=(0,1,0), material=materials.rough)
mf.rotate(axis=(0,0,1), angle=-pi/2)
mf.pos = (-4.1,0,0)
cre.visible=0
del(cre)
pause()
lbl.text = "Let's have a look at the inside\nmh.start = 2\nmh.end = -9"
mh.start = 2
mh.end = -9
pause()
lbl.text = "Let's close it again\nmh.start =0\nmh.end = -1"
mh.start =0
mh.end = -1
pause()
lbl.text = "We can even animate the cover opening"
mh.start = 2
for i in range(-1, -16,-1):
    mh.end = i
    rate(16)
pause()
for i in range(-16, -8,+1):
    mh.end = i
    rate(16)
pause()
lbl.text = "Now it is time to add a little gear on the shaft\n\nFor visibility purposes, let's hide some parts for the moment"
mh.visible=0
rtr1.visible=0
rtr2.visible=0
shft.visible=0
pause()
lbl.text = "Let's create a small gear to fit on the shaft\n\ng = shapes.gear(radius=1.5, n=8, addendum=0.2, dedendum=0.2)"
g = shapes.gear(radius=1.5, n=8, addendum=0.2, dedendum=0.2)
gc = extrusion(shape=g)
pause()
g -= shapes.circle(radius=0.75)
lbl.text = "Subtract a hole for the shaft\n\ng -= shapes.circle(radius=0.75)"
gc.visible=0
gc = extrusion(shape=g)
gf = frame()
pause()
lbl.text = "Now we can extrude the shape to obtain the gear in place\n\nge = extrusion(pos=[(8.5,0,0),(10.,0,0)], shape=g, material=materials.rough, frame=gf)"
ge = extrusion(pos=[(8.5,0,0),(10.,0,0)], shape=g, material=materials.rough, frame=gf)
gc.visible=0
mh.visible=1
rtr1.visible=1
rtr2.visible=1
shft.visible=1
pause()
lbl.text = "We get a conical gear if we set\n\nge.scale[1] = 0.7"
ge.scale[1] = 0.7
pause()
lbl.text = "... and we get a helical gear if we set\n\nge.twist = 0.3"
ge.twist = 0.3
pause()
for i in range(1,len(scene.objects)):
    try:
        o = scene.objects[1]
        o.visible = 0
        del(o)
    except: continue
lbl.text = "A WINE BOTTLE"
pause()
scene.range = 25
scene.center = (0,+5,0)
lbl.yoffset = 400
lbl.text = "Let's start with a rectangle again\n\nr = shapes.rectangle(height=24, width=7.5, roundness=0.35)"
r1 = shapes.rectangle(height=24, width=7.5, roundness=0.35)
re1 = extrusion(shape=r1)
pause()
lbl.text = "Add a rectangle\n\nr = shapes.rectangle(height=10, width=2.5, pos=(0,14))"
r2 = shapes.rectangle(height=10, width=2.5, pos=(0,14))
re2 = extrusion(shape=r2)
pause()
lbl.text = "Add another small one\nso we obtain a bottle profile\nr = shapes.rectangle(height=0.75, width=3, pos=(0,18))"
r3 = shapes.rectangle(height=0.75, width=3.0, pos=(0,18))
re3 = extrusion(shape=r3)
br1 = r1+r2+r3
re1.visible=0
re2.visible=0
re3.visible=0
del(re1)
del(re2)
del(re3)
bre1 = extrusion(shape=br1)
pause()
lbl.text = "Cut the bottom out a bit, to get a flat bottom\n\nbr2 = (r1+r2+r3)-shapes.rectangle(height=1, width=8, pos=(0,-11.6)"
sbb = shapes.rectangle(height=1, width=8, pos=(0,-11.6))
br2 = br1-sbb
bre1.visible=0
del(bre1)
cc = curve(pos=[(0,-13,0),(0,18,0)], color=(1,0,0))
bre2 = extrusion(shape=br2)
pause()
lbl.text = "Cut the left side out\n\nbr3 = br2-shapes.rectangle(height=45, width=8, pos=(-4,0))"
shb = shapes.rectangle(height=45, width=8, pos=(-4,0))
bre2.visible=0
del(bre2)
br3 = br2-shb
bre3 = extrusion(shape=br3)
pause()
lbl.text = "We can extrude this polygon to get a bottle\nbut it will be a solid one, not a hollow one\nWe need a different solution"
bp = br3.contour(0)[20:21] + br3.contour(0)[0:19]
pause()
bpc = curve(pos=bp, radius=0.1, color=(0,0,1))
lbl.text = "We obtain an open contour, by omitting the point in the middle of the bottle mouth\n\nbp = br3.contour(0)[20:21] + br3.contour(0)[0:19]"
pause()
bb = box(size=(2,2,2), color=(1,1,0))
bpc.visible=0
bre3.visible=0
lbl.text = "We rotate this open curve around the y axis to obtain a hollow bottle\n\nbpe = extrusion(pos=paths.arc(angle1=0, angle2=-2*pi, shape=bp, radius=0.001), color=(0,1,0.8), material=materials.glass)"
bpe = extrusion(pos=paths.arc(angle1=0, angle2=-2*pi, radius=0.001), shape=bp, color=(0,1,0.8), material=materials.glass)
pause()
lbl.text = "Let's empty the bottle and add some wine\n\nwine = extrusion(pos=[(0,-9.5,0),(0,2,0)], shape=shapes.circle(radius=3.74), material=materials.ice, color=(0.9,1,0.8))"
bpc.visible=0
bre3.visible=0
del(bpc)
del(bre3)
wine = extrusion(pos=[(0,-9.5,0),(0,2,0)], shape=shapes.circle(radius=3.74), material=materials.ice, color=(0.9,1,0.8))
bpe.visible=0
bpe.visible=1
bb.visible=0
cc.visible=0
pause()
for i in range(len(scene.objects)):
    o = scene.objects[0]
    o.visible = 0
    del(o)
chrs = extrusion(shape="cheers !")
