
from __future__ import division
from visual import *
from time import clock

# A tutorial on the extrusion object
# Bruce Sherwood, January 2011

scene.width = 600
scene.height = 800
scene.background = color.white
scene.foreground = color.black
scene.userspin = False
scene.userzoom = False
scene.fov = 0.4
scene.range = 14

contour1 = [(0,-5), (-3,3), (3,3)]
contour2 = [(-2,2.5), (0,5), (2,2.5)]
contour3 = [(-2,2), (2,2), (.5,-2), (-.5,-2)]

class main():
    def __init__(self, npages):
        self.npages = npages
        self.page = 1
        self.jumpenabled = False

    def showpages(self):
        self.y = -13
        self.dy = .7
        self.w = 12
        self.dx = self.w/self.npages
        self.x0 = -self.w/2
        if self.jumpenabled:
            box(pos=(0,self.y,0), size=(self.w,self.dy,.01), color=color.gray(.9))
            box(pos=(self.x0+(self.page-.5)*self.dx,self.y,.02), size=(self.dx,self.dy,.01), color=color.gray(.5))
            label(pos=(self.x0,self.y), text="Choose a page:", xoffset=-1, opacity=0, box=0, line=0)
            for p in range(self.npages):
                L = label(pos=(self.x0+(p+.5)*self.dx,self.y), opacity=0, box=0, line=0)
                L.text = "%d" % (p+1)

    def checkjump(self, mousepos):
        if not self.jumpenabled: return None
        if (self.y-self.dy/2 <= mousepos.y <= self.y+self.dy/2) and (self.x0 <= mousepos.x <= self.x0+self.npages*self.dx):
            return (mousepos.x-self.x0)//self.dx+1
        else:
            return None # no page change
       
    def pause(self, dt=None): # returns True if jump to new page
        t0 = clock()
        while True:
            rate(30)
            if scene.mouse.events:
                m = scene.mouse.getevent()
                if m.click == 'left':
                    # check for choosing a new page
                    newpage = self.checkjump(m.project(normal=(0,0,1)))
                    if newpage is None:
                        return False
                    else:
                        self.page = newpage
                        return True
            elif scene.kb.keys:
                k = scene.kb.getkey()
                return False
            elif dt:
                if clock()-t0 >= dt:
                    return False

    def jump(self, page):
        for obj in scene.objects:
            obj.visible = False
            del obj
        scene.mouse.events = 0
        while scene.kb.keys > 0:
            key = scene.kb.getkey()
        self.page = page
        self.showpages()

    def spin(self, thing, origin, dynamic=False):
        origin = vector(origin)
        spin = False
        if dynamic:
            R = 6
            dtheta = pi/20
            arc = arange(.3,3.2*pi/4,dtheta)
            t = 0
        while True:
            rate(200)
            if scene.kb.keys:
                scene.kb.getkey()
                return False
            elif scene.mouse.events:
                m = scene.mouse.getevent()
                if m.click == 'left':
                    newpage = self.checkjump(m.project(normal=(0,0,1)))
                    if newpage is None:
                        return False
                    else:
                        self.page = newpage
                        return True
                elif m.drag == 'right':
                    spin = True
                    lastray = scene.mouse.ray
                    scene.cursor.visible = False
                elif m.drop == 'right':
                    spin = False
                    scene.cursor.visible = True
            elif spin:
                if dynamic:
                    change = thing.frame
                else:
                    change = thing
                newray = scene.mouse.ray
                dray = newray-lastray
                right = newray.cross(change.up).norm() # unit vector to the right
                anglex = 20*arcsin(dray.dot(right))
                change.rotate(angle=anglex, axis=change.up, origin=origin)
                angley = -20*arcsin(dray.dot(change.up))
                maxangle = scene.up.diff_angle(change.up)
                newup = change.up.rotate(angle=angley, axis=right)
                newangle = scene.up.diff_angle(newup)
                if newangle < pi/2:
                    change.rotate(angle=angley, axis=right, origin=origin)
                lastray = newray
            if dynamic: 
                thing.x = R*cos(arc)*(1+.3*sin(t))
                thing.z = -R*sin(arc)*(1+.3*sin(.5*t))
                thing.twist = .05*sin(t)
                thing.initial_twist = -.2*sin(t)
                thing.up = (0,.4+.2*sin(1.1*t),.6+.4*cos(1.5*t))
                thing.xscale = 1+.6*sin(2*t)
                t += .01

def makelabel(x=0, y=0, centered=False):
    if centered:
        return label(pos=(x,y), opacity=0, box=0, line=0)
    else:
        return label(pos=(x,y), xoffset=1, opacity=0, box=0, line=0)

def drawcontour(origin, contour, ccolor):
    origin = vector(origin)
    p1 = points(size=8, color=color.red)
    curve1 = curve(color=ccolor)
    for pt in contour:
        pv = vector(pt)
        p1.append(origin+pv)
        curve1.append(vector(origin+pv)-vector(0,0,.1))
        if pages.pause(.25): return True
    curve1.append(origin+vector(contour[0])-vector(0,0,.1))
    return False

#-------------------------------------------------------------------------
def intro():
    L1 = makelabel(-10,12)
    L1.text = """
This is an overview on how to make an extrusion object like the one shown here.
More information is in the detailed documentation installed with VPython.

This object consists of a 2D shape and an extrusion path.
Click or press a key to proceed.
"""
    square = shapes.rectangle(width=4)
    hole1 = shapes.circle(pos=(.7,.7), radius=.7)
    hole2 = Polygon([(-1.2,0.8), (1.6,-1.5), (-1.2,-1.5)])
    disk = shapes.circle(pos=(0,2), radius=1)
    f = frame()
    P = paths.arc(pos=(-1.5,2.5,0), radius=6, np=5*32, angle1=.3, angle2=3.2*pi/4)
    path = list(P.pos)
    P0 = vector(path[0])
    path.insert(1,P0+0.01*norm(vector(path[1])-P0))
    E = extrusion(frame=f, pos=path,
              color=(0.904,0.693,0.595), material=materials.plastic, shape=square+disk-hole1-hole2, scale=1.6)
    f.rotate(angle=pi/10, axis=(1,0,0), origin=(0,0,0))
    if pages.pause(): return
    E.end = 1
    L2 = makelabel(0,-2, centered=True)
    L2.text = """
Make a 2D shape with easy-to-use tools that are provided.
"""
    if pages.pause(): return
    L2.text = "Then extrude this 2D shape along a path."
    curve(frame=f, pos=path, color=color.blue)
    if pages.pause(): return
    for i in range(1,len(E.pos)):
        rate(20)
        E.end = i
    L2.pos = (0,-9)
    pages.jumpenabled = True
    pages.showpages()
    L2.text = """
Rotate the object to examine this extrusion.

Throughout this overview, click or press a key to proceed,
or click on a page number to jump to any page.
"""
    if not pages.spin(f, (0,0,0)): pages.page += 1

#-------------------------------------------------------------------------
def contours():
    L1 = makelabel(-10.5,11.7)
    L1.text = """
The first step in making an extrusion
is to create a 2D shape to extrude.

We specify a contour \n(a closed path of 2D points):
"""
    axes = curve(pos=[(0,13.5), (0,8), (5,8)])
    xaxis = makelabel(axes.x[0], axes.y[0])
    xaxis.text = " y"
    yaxis = makelabel(axes.x[2], axes.y[2])
    yaxis.text = " x"
    if pages.pause(): return
    if drawcontour((0,8), contour1, color.blue): return
    if pages.pause(): return
    L1.text = "We'll"+' refer to this contour as "c1".'
    if pages.pause(): return
    L2 = makelabel(2,12)
    L2.text = 'Specify another contour "c2".'
    if drawcontour((0,8), contour2, color.orange): return
    if pages.pause(): return
    L3 = makelabel(1.5,6)
    L3.text = 'Specify another\ncontour "c3".'
    if drawcontour((0,8), contour3, (0,.5,0)): return
    if pages.pause(): return
    lab1 = makelabel(-10,.5)
    lab1.text = """
We can make these contours using the Polygon function, by specifying
lists of 2D points in the xy plane (or choose from a library of shapes):

c1 = Polygon( [ (0,-5), (-3,3), (3,3) ] )   # 3 points for lower triangle
c2 = Polygon( [ (-2,2.5), (0,5), (2,2.5) ] )      # upper triangle
c3 = Polygon( [ (-2,2), (2,2), (.5,-2), (-.5,-2) ] )   # the trapezoid
"""
    if pages.pause(): return
    L4 = makelabel(-10,-6)
    L4.text = """
The Polygon module imported by VPython
makes it possible to add or subtract such
contours to make a compound 2D surface.

For example, c1+c2-c3 yields a 2D surface
with a hole:
"""
    if pages.pause(): return
    c1 = Polygon(contour1)
    c2 = Polygon(contour2)
    c3 = Polygon(contour3)
    extrusion(pos=(4,-7,0), color=color.gray(.7), shape=c1+c2-c3)
    if not pages.pause(): pages.page += 1

#-------------------------------------------------------------------------
def extrude():
    c1 = Polygon(contour1)
    c2 = Polygon(contour2)
    c3 = Polygon(contour3)
    f1 = frame(pos=(-6,6,0))
    f1.rotate(axis=(1,0,0), angle=pi/15)
    f1.rotate(axis=(0,1,0), angle=pi/80)
    E1 = extrusion(frame=f1, pos=[(0,0,0), (0,0,-8)],
                shape=c1+c2-c3, color=color.orange)
    E1.scale = 0.8
    L1 = makelabel(-10,12)
    L1.text = """
The 2D shape created by "c1+c2-c3" can be extruded, like this:

extrusion(pos=[(0,0,0), (0,0,-8)], shape=c1+c2-c3, color=color.orange)
"""
    if pages.pause(): return
    points(frame=f1, pos=E1.pos, size=8, color=color.red)
    curve(frame=f1, pos=E1.pos, color=color.blue)
    L1b = makelabel(-3.5,6)
    L1b.text = """
The pos attribute is like that of a curve object,
a list of points (or choose a path from a library).

The first point (0,0,0) is at the front, and
the second point (0,0,-8) is at the back.
These points are indicated here by red dots.

The xy positions in the shape are relative to
the pos locations. Usually the shape's center
should be near (x,y) = (0,0).
"""
    if pages.pause(): return
    L2 = makelabel(-10.5,-.5)
    L2.text = """
Rotate the object to examine this multipoint extrusion, with points shown:

extrusion(pos=[(0,0,0),(-1.2,0,-2.9),(-4.1,0,-4.0),(-7.0,0,-2.7),(-8,0,-0.2)],
                shape=c1+c2-c3, color=color.orange)
"""
    f2 = frame(pos=(2,-8,0))
    f2.rotate(axis=(1,0,0), angle=pi/30)
    f2.rotate(axis=(0,1,0), angle=-pi/10)
    E2 = extrusion(frame=f2, pos=[(0,0,0),(-1.2,0,-2.9),(-4.1,0,-4.0),(-7.0,0,-2.7),(-8,0,-0.2)],
                shape=c1+c2-c3, color=color.orange)
    E2.scale = 0.8
    points(frame=f2, pos=E2.pos, size=8, color=color.red)
    curve(frame=f2, pos=E2.pos, color=color.blue)
    if not pages.spin(f2, (0,-8,0)): pages.page += 1

#-------------------------------------------------------------------------
def shapelibrary():
    L1 = makelabel(-10,10)
    L1.text = """
It can be tedious to create lists of xy points to make a shape, or
a list of points for the pos path along which the extrusion is made.

For that reason there is a library of ready-made shapes, and a
library of ready-made paths.

Rotate this extrusion of a triangle along a closed pentagonal path:

      E = extrusion(pos=paths.pentagon(pos=(0,2.5,0), length=5),
          shape=shapes.triangle(length=3), color=color.cyan)
"""
    f = frame()
    E = extrusion(frame=f, pos=paths.pentagon(pos=(0,2.5,0),length=5), shape=shapes.triangle(length=3),
                  color=color.cyan)
    f.rotate(angle=pi/5, axis=(1,0,0), origin=(0,2.5,0))
    if pages.spin(f, (0,2.5,0)): return
    L2 = makelabel(-10,-3)
    L2.text = """
The "paths" library contains useful paths that you can assign to "pos".
Here we have a closed pentagonal path whose center is at (0,2.5,0). 
Each side is of length 5.
"""
    if pages.spin(f, (0,2.5,0)): return
    L3 = makelabel(-10,-6)
    L3.text = """
The "shapes" library contains useful shapes that you can assign to "shape".
Here we have specifed a triangle of length 3 as the cross section.

See the detailed documentation for what paths and shapes are available.
"""
    if pages.spin(f, (0,2.5,0)): return
    L3 = makelabel(-10, -9)
    L3.text = """
The paths library provides paths in the xz plane, as in the example above.
In the next section we'll show how to orient the path differently.
"""
    if not pages.spin(f, (0,2.5,0)): pages.page += 1

#-------------------------------------------------------------------------
def pathorientation():
    L1 = makelabel(-10,11)
    L1.text = """
A shape object is a 2D object, and its coordinates are given in the xy plane.

Currently, the points provided by the paths library are also 2D and can most
usefully be thought of as being created in the xy plane, like shapes: 
"""
    h = 2
    x = curve(pos=[(-5,h+2,0), (5,h-2,0)], color=color.black)
    theta = atan((x.y[1]-x.y[0])/(x.x[1]-x.x[0]))
    y = curve(pos=[(0,h-2,0), (0,h+6,0)], color=color.black)
    z = curve(pos=[(-2.5,h-2,0), (5,h+2+2,0)], color=color.black)
    Lx = makelabel(4.5,h-2.3)
    Lx.text = "x"
    Ly = makelabel(.1,h+6)
    Ly.text = "y"
    Lz = makelabel(-2.2,h-2)
    Lz.text = "z"
    d = 3
    f = frame(pos=(0,h))
    base = curve(frame=f, x=[-d*cos(theta),d*cos(theta)], y=[-d*sin(theta),+d*sin(theta)],
            color=color.red, radius=.1)
    R = 5
    c = curve(frame=f, pos=[base.pos[0], (0,R,0), base.pos[1]], color=color.red, radius=.1)
    if pages.pause(): return
    L2 = makelabel(-10,-3)
    L2.text = """
After creation, the path in the xy plane is tipped backwards onto the xz plane,
with the top of the path in the -z direction.
"""
    if pages.pause(): return
    N = 50
    dtheta = .288*pi/N
    for i in range(N):
        rate(N/2)
        c.pos[1] = (R*sin(i*dtheta),R*cos(i*dtheta),0)
    L3 = makelabel(-10,-6)
    L3.text = """
Although the paths library produces paths in the xz plane, it is easy to
reorient the path by specifying the normal to the desired plane of the path.
For example the following statement would make a path perpendicular to the
x axis, by specifying that 'up' is in the (1,0,0) direction:

    p = paths.triangle(length=2, up=(1,0,0))
"""
    if pages.pause(): return
    N = 50
    dtheta = .39*pi/N
    for i in range(N):
        rate(N/2)
        base.pos = [(-d*cos(theta-i*dtheta),-d*sin(theta-i*dtheta)),(d*cos(theta-i*dtheta),d*sin(theta-i*dtheta))]
        c.pos[0] = base.pos[0]
        c.pos[2] = base.pos[1]
    arr = arrow(pos=(1.5,h+1.5), axis=3*norm(x.pos[1]-x.pos[0]), color=color.green)
    Larr = makelabel(arr.x+arr.axis.x+.1,arr.y+arr.axis.y)
    Larr.text = "(1,0,0)"
    L4 = makelabel(-10,-10)
    L4.text = """
For more information, see the detailed documentation.
"""
    if not pages.pause(): pages.page += 1

#-------------------------------------------------------------------------
def scaling():
    L1 = makelabel(-10,12)
    L1.text = """
The shape that is the cross section of the extrusion object can be scaled
in x or y, all along the path specified by the pos points.

Here is an extrusion with varying scale factors. Rotate the object.
"""
    L2 = makelabel(-10,-5)
    L2.text = """
r = shapes.rectangle(width=10) # a 10 by 10 square
h = shapes.circle(radius=4)
E = extrusion(pos=[(0,4,4), (0,4,-4)], shape=r-h, color=color.red,
                  scale=[(1.5,1.0), (0.5,0.3)])

At the first point (0,4,4) the xscale is 1.5 and the y scale is 1.0.
At the second point (0,4,-4) the xscale is 0.5 and the y scale is 0.3.
"""
    r = shapes.rectangle(width=10)
    h = shapes.circle(radius=3)
    f = frame()
    E = extrusion(frame=f, pos=[(0,4,4), (0,4,-4)], shape=r-h, color=color.red,
                  scale=[(1.5,1), (0.5,0.3)])
    f.rotate(angle=-pi/6, axis=(0,1,0), origin=(0,4,0))
    if pages.spin(f, (0,0,0)): return
    L3 = makelabel(-10,-10)
    L3.text = """
The same effect could have been achieved with xscale=[1.5,0.5] and
yscale=[1.0,0.3]; you can scale x and y separately. Note that the
circle has been squashed into an ellipse.

If you want to set the same scale factor for all points along the path,
just say scale=2 (scales both x and y), or xscale=0.7, or yscale=1.3.
"""
    if not pages.spin(f, (0,0,0)): pages.page += 1

#-------------------------------------------------------------------------
def twisting():
    L1 = makelabel(-10,12)
    L1.text = """
You can also twist along the path. Here is an example you can rotate:

extrusion(pos=paths.circle(radius=8, np=400), twist=2*pi/200,
              shape=shapes.rectangle(width=3, height=1.5), color=color.green)
"""
    f = frame()
    E = extrusion(frame=f, pos=paths.circle(pos=(0,2,0), radius=7, np=400), twist=2*pi/200,
              shape=shapes.rectangle(width=3, height=1.5), color=color.green)
    f.rotate(angle=pi/6, axis=(1,0,0), origin=(0,2,0))
    if pages.spin(f, (0,2,0)): return
    L2 = makelabel(-10,-9)
    L2.text = """
We've chosen a circular path made of 400 points (np=400), and we've
imposed a twist of 2*pi/200 radians from one point to the next along
the path. There are two full twists around the circle.

The twist attribute is actually an array with as many elements as pos.
Setting twist=2*pi/200 sets all elements of the array to 2*pi/200, so that
the twist from one point to the next is 2*pi/200 all along the path.
"""
    if not pages.spin(f, (0,2,0)): pages.page += 1

#-------------------------------------------------------------------------
def dynamic():
    L1 = makelabel(-10,8)
    L1.text = """
You can dynamically change the extrusion parameters, with dramatic results.

Here the path, twist, xscale, and up are all being changed simultaneously.
"""
    square = shapes.rectangle(width=4)
    hole1 = shapes.circle(pos=(.7,.7), radius=.7)
    hole2 = Polygon([(-1.2,0.8), (1.6,-1.5), (-1.2,-1.5)])
    disk = shapes.circle(pos=(0,2), radius=1)
    R = 6
    dtheta = pi/20
    arc = arange(.3,3.2*pi/4,dtheta)
    f = frame()
    E = extrusion(frame=f, x=R*cos(arc), y=0, z=-R*sin(arc),
                  color=(0.904,0.693,0.595), material=materials.plastic,
                  shape=square+disk-hole1-hole2, scale=1.6)
    if pages.spin(E, (0,0,0), True): return
    L2 = makelabel(-10,-8)
    L2.text = """
This works because the 3D rendering of an extrusion object is quite fast.
"""
    if not pages.spin(E, (0,0,0), True): pages.page += 1

#-------------------------------------------------------------------------
def miscellaneous():
    L1 = makelabel(-10, 1)
    L1.text = """
Here are additional attributes of the extrusion object.
See the detailed documentation for more information.


initial_twist
The first element of the twist array is ignored. If you need to twist
the initial face, set initial_twist. Alternatively, you could change
the "up" attribute (see documentation on the box object).


start, end
Choose which point along the pos curve to begin the display, and at
which point along the pos curve to end the display. Points before
start or after end are not shown on the screen. The default values
are start = 0 (pos[0]) and end = -1 (pos[-1] is the last point).


show_start_face, show_end_face
These are normally True. If you don't want a face at location start
or end to be shown, set the corresponding attribute to False. This
exposes the interior of the extrusion.


first_normal, last_normal
These read-only attributes give you the normals to the first (start=0)
and last faces (end=-1), whether or not these faces are actually shown;
these may be useful if you are joining an extrusion to another object.


append
There is an append option similar to that of the curve object.


smooth
By default, normals to the surfaces are averaged if their dot products
(the cosine of the angle between them) are greater or equal to 0.95,
which corresponds to an angular difference of 18 degrees. The effect
is to smooth away sharp breaks between two surfaces whose normals
don't differ by much. Setting smooth=0.9 will smooth adjoining surfaces
whose orientation differs by 53 degrees, a much looser criterion.
"""
    if not pages.pause(): pages.page += 1

#-------------------------------------------------------------------------
def composites():
    L1 = makelabel(-10,12)
    L1.text = """
It can be useful to make composites from two or more extrusion objects.
Suppose you want a straight hole drilled through a tapered solid. Rotate
these two extrusions, one tapered (with tapered hole), the other not:
"""
    fall = frame()
    f1 = frame(frame=fall, pos=(-3,5,0))
    E1 = extrusion(frame=f1, pos=[(0,0,4), (0,0,-4)], shape=shapes.rectangle(width=7)-shapes.circle(radius=1.5),
          color=color.red)
    E1.scale[1] = .5
    cylinder(frame=f1, pos=(0,0,5), radius=0.5, axis=(0,0,-10), color=color.cyan)
    f2 = frame(frame=fall, pos=(3,5,0))
    E2 = extrusion(frame=f2, pos=E1.pos, shape=shapes.circle(radius=1.55)-shapes.circle(radius=0.7), color=E1.color)
##    E2 = extrusion(frame=f2, pos=E1.pos, shape=shapes.circle(radius=1.5)-shapes.circle(radius=1.0), color=color.yellow)
##    E2.scale[1] = 0.5
    if pages.spin(fall, fall.pos): return
    L2 = makelabel(-10,-6)
    L2.text = """
Next we'll place these two extrusions in the same place.
"""
    if pages.spin(fall, fall.pos): return
    f1.pos = f2.pos = (0,5,0)
    L2.text = "Rotate and observe a tapered solid with a straight hole."
    if not pages.spin(fall, fall.pos): pages.page += 1

#-------------------------------------------------------------------------
def composites2():
    L1 = makelabel(-10,12)
    L1.text = """
Another use for composite extrusions is to specify different colors.
Here is a tapered hollow yellow cylinder and a tapered red solid.
"""
    fall = frame()
    f1 = frame(frame=fall, pos=(-3,5,0))
    E1 = extrusion(frame=f1, pos=[(0,0,4), (0,0,-4)], shape=shapes.rectangle(width=7)-shapes.circle(radius=1.5),
          color=color.red)
    E1.scale[1] = .5
    cylinder(frame=f1, pos=(0,0,5), radius=0.5, axis=(0,0,-10), color=color.cyan)
    f2 = frame(frame=fall, pos=(3,5,0))
    E2 = extrusion(frame=f2, pos=E1.pos, shape=shapes.circle(radius=1.5)-shapes.circle(radius=1.0), color=color.yellow)
    E2.scale[1] = 0.5
    if pages.spin(fall, fall.pos): return
    L2 = makelabel(-10,-6)
    L2.text = """
Next we'll place these two extrusions in the same place.
"""
    if pages.spin(fall, fall.pos): return
    f1.pos = f2.pos = (0,5,0)
    L2.text = "Rotate and observe the composite of red solid and yellow insert."
    if not pages.spin(fall, fall.pos): pages.page += 1

#-------------------------------------------------------------------------
def pathologies():
    L1 = makelabel(-10,10)
    L1.text = """
A sharp bend in the path can cause a later segment to overlap an earlier
segment. Consider the following two cases. Rotate the objects to see the
strange behavior of the extrusion on the right. The bend is so sharp that
the second segment intersects the first.
"""
    fall = frame(pos=(0,1,0))
    f1 = frame(frame=fall, pos=(8,0,0))
    E1 = extrusion(frame=f1, pos=[(-15,0,0), (-15,3,0), (-15,3,0), (-11,1,0)], shape=shapes.rectangle(width=3,height=2),
          color=[color.red, color.red, color.cyan, color.cyan])
    curve(frame=f1, pos=E1.pos+vector(0,0,1), radius=0.1, color=color.yellow)
    f2 = frame(frame=fall, pos=(18,0,0))
    E2 = extrusion(frame=f2, pos=[(-15,0,0), (-15,3,0), (-15,3,0), (-11,-2,0)], shape=shapes.rectangle(width=3,height=2),
          color=[color.red, color.red, color.cyan, color.cyan])
    curve(frame=f2, pos=E2.pos+vector(0,0,1), radius=0.1, color=color.yellow)
    fall.rotate(angle=-pi/4, axis=(1,0,0), origin=(0,0,0))
    if pages.spin(fall, fall.pos): return
    L2 = makelabel(-10,-6)
    L2.text = """
Evidently it is important not to create very sharp bends in wide extrusions.
"""
    if pages.spin(fall, fall.pos): return
    L3 = makelabel(-10,-8)
    L3.text = """
This is the end of the overview. See the detailed VPython documentation for
more details.
"""
    if not pages.pause(): pages.page = 0
    
#-------------------------------------------------------------------------
pages = main(12)
startpage = 1
pages.page = startpage
if startpage != 1:
    pages.jumpenabled = True
    pages.showpages()
while True:
    if pages.page == 1:
        pages.jump(1)
        intro()
    elif pages.page == 2:
        pages.jump(2)
        contours()
    elif pages.page == 3:
        pages.jump(3)
        extrude()
    elif pages.page == 4:
        pages.jump(4)
        shapelibrary()
    elif pages.page == 5:
        pages.jump(5)
        pathorientation()
    elif pages.page == 6:
        pages.jump(6)
        scaling()
    elif pages.page == 7:
        pages.jump(7)
        twisting()
    elif pages.page == 8:
        pages.jump(8)
        dynamic()
    elif pages.page == 9:
        pages.jump(9)
        miscellaneous()
    elif pages.page == 10:
        pages.jump(10)
        composites()
    elif pages.page == 11:
        pages.jump(11)
        composites2()
    elif pages.page == 12:
        pages.jump(12)
        pathologies()
    else:
        pages.page += 1

    
