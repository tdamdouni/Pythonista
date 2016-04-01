
from visual import *
import time

print("""
Press to enter roaming mode, release to exit roaming mode.
In roaming mode, with the mouse button down, move the mouse
above or below the center of the scene to move forward or
backward; right or left rotates your direction of motion.
""")

# Bruce Sherwood

# A surreal scene that illustrates many of the features of VPython

def hourminute():
    now = time.localtime(time.time())
    hour = now[3] % 12
    minute = now[4]
    return (hour, minute)

class analog_clock:
    def __init__(self, pos=(0,0,0), radius=1., axis=(0,0,1)):
        self.pos = vector(pos)
        self.axis = vector(axis)
        self.radius = radius
        self.spheres = []
        self.hour = 0
        self.minute = -1
        for n in range(12):
            self.spheres.append(sphere(pos=self.pos+rotate(radius*scene.up,
                    axis=self.axis, angle=-2.*pi*n/12.), radius=radius/20.,
                    color=color.hsv_to_rgb((n/12.,1,1)) ))
        self.hand = arrow(pos=pos, axis=0.95*radius*scene.up,
                    shaftwidth=radius/10., color=color.cyan)
        self.update()
        
    def update(self):
        hour, minute = hourminute()
        if self.hour == hour and self.minute == minute: return
        self.hand.axis = rotate(0.95*self.radius*scene.up,
                    axis=self.axis, angle=-2.*pi*minute/60.)
        self.spheres[self.hour].radius = self.radius/20.
        self.spheres[hour].radius = self.radius/10.
        self.hour = hour
        self.minute = minute

scene.title = "Surreal Stonehenge"
##scene.stereo = 'redcyan'
scene.height = 600
scene.width = 600
scene.range = (1,1,1)
scene.center = (0,2,20)
scene.userspin = False
scene.userzoom = False
grey = (0.8, 0.8, 0.8)
Nslabs = 8
R = 10
w = 5
d = 0.5
h = 5
photocenter = 0.15*w

# The floor, central post, and ball atop the post
floor = box(pos=(0,-0.1,0),size=(.2,24,24), axis=(0,1,0), color=color.orange, material=materials.wood)
pole= cylinder(pos=(0,0,0),axis=(0,h,0), radius=0.2, color=(1,0,0))
sphere(pos=(0,h,0), radius=0.5, color=(1,0,0))

# Set up the gray slabs, including a portal

### Here is the code used to create the cactus flower display
##import Image # Must install PIL, the Python Imaging Library
##name = "flower"
##width = 128 # must be power of 2
##height = 128 # must be power of 2
##im = Image.open(name+".jpg")
###print im.size # optionally see size of image
### Optional cropping:
###im = im.crop((x1,y1,x2,y2)) # (0,0) is upper left
##im = im.resize((width,height), Image.ANTIALIAS)
##materials.saveTGA(name,im)

for i in range(Nslabs):
    theta = i*2*pi/Nslabs
    c = cos(theta)
    s = sin(theta)
    xc = R*c
    zc = R*s
    if i == 2: # Make a portal
        box(pos=(-3.*w/8.,0.75*h/2.,R),
            length=0.5*w/2,height=0.75*h,width=d, color=grey)
        box(pos=(3.*w/8.0,0.75*h/2.,R),
            length=0.5*w/2,height=0.75*h,width=d, color=grey)
        box(pos=(0,0.85*h,R),
            length=w,height=0.3*h,width=d, color=grey)
        
    else:
        slab = box(pos=(R*c, h/2., R*s), axis=(c,0,s),
                   size=(d,h,w), color=grey)
        if i == 0:
            photo = materials.texture(data=materials.loadTGA("flower128"), mapping="rectangular")
        if i != 6:
            for x in range(2):
                for y in range(2):
                    box(pos=slab.pos+vector(-s*photocenter*(2*x-1),photocenter*(2*y-1),c*photocenter*(2*x-1)),
                        size=(1.1*d,0.9*2*photocenter,0.9*2*photocenter), axis=(c,0,s),
                        material=photo)

# Decorate back slab with a gold box and a clock
box(pos=(0,h/2.,-R+d/2+0.1), size=(w/2.,w/2.,0.2), 
    color=(1,0.8,0), material=materials.wood)
clock = analog_clock(pos=(0,h/2.,-R+d/2+0.2+0.2*h/10),
                     radius=0.2*w, axis=(0,0,1))
                     
# Draw guy wires from the top of the central post
Nwires = 32
for i in range(Nwires):
    theta = i*2*pi/Nwires
    cylinder(pos=(0,h,0), axis=(R*cos(theta),-h-0.1,R*sin(theta)),
             radius=0.02, color=(1,0.7,0))

# Display a pyramid
pyramid(pos=(-4,0,-5), size=(2,2,2), axis=(0,3,0), color=(0,0.6,0), material=materials.marble)

# Display smoke rings rising out of a black tube
smoke = []
Nrings = 20
x0, y0, z0 = -5, 1.5, -2
r0 = 0.1
spacing = 0.2
thick = r0/4
dr = 0.015
dthick = thick/Nrings
gray = 1
cylinder(pos=(x0,0,z0), axis=(0,y0+r0,0), radius=1.5*r0, color=color.black)

# Create the smoke rings
for i in range(Nrings):
  smoke.append(ring(pos=(x0,y0+spacing*i,z0), axis=(0,1,0),
                  radius=r0+dr*i, thickness=thick-dthick*i, color=(gray,gray,gray)))
y = 0
dy = spacing/20
top = Nrings-1

# Roll a log back and forth
rlog = 1
wide = 4
zpos = 2
zface = 5
tlogend = 0.2
v0 = 1
v = v0
omega = -v0/rlog
theta = 0
dt = 0.1
tstop = 0.3
log = frame(pos=(-wide,rlog,zpos), axis=(0,0,1))
cylinder(frame=log,
         pos=(0,0,0), axis=(zface-zpos,0,0),
         color=(0.8,0.5,0), opacity=0.5)
box(frame=log,
    pos=(zface-zpos+tlogend/2.+.01,0,0), axis=(0,0,1),
    length=rlog, height=rlog, width=tlogend,
    color=color.yellow, opacity=0.5)

leftstop = box(pos=(-wide-rlog-tstop/2,0.6*rlog,(zpos+zface)/2),
    length=tstop, height=1.2*rlog, width=(zface-zpos), color=color.red)
rightstop = box(pos=(wide+rlog+tstop/2,0.6*rlog,(zpos+zface)/2),
    length=tstop, height=1.2*rlog, width=(zface-zpos), color=color.red)

# Run a ball up and down the pole
y1 = 0.2*h
y2 = 0.7*h
rball = 0.4
cylinder(pos=(0,y1-0.9*rball,0), axis=(0,0.1,0), radius=1.3*pole.radius, color=color.green)
cylinder(pos=(0,y2+0.9*rball,0), axis=(0,0.1,0), radius=1.3*pole.radius, color=color.green)
vball0 = 0.3*v0
vball = vball0
ballangle = 0.05*pi
ball = frame(pos=(0,y1,0))
sphere(frame=ball, radius=rball, color=color.blue)
for nn in range(4):
    cc = cone(frame=ball, pos=(0.8*rball,0,0), axis=(3*rball,0,0), radius=0.5*rball, color=color.yellow)
    cc.rotate(angle=0.5*nn*pi, axis=(0,1,0), origin=(0,0,0))
rbaseball = 0.3
vbaseball0 = 3*v0

# Display an ellipsoid
Rcloud = 0.8*R
omegacloud = v0/Rcloud
cloud = ellipsoid(pos=(0,0.7*h,-Rcloud), size=(5,2,2),
                  color=(1,0.5,0.5), opacity=0.3)

rhairs = 0.025 # half-length of crosshairs
dhairs = 2 # how far away the crosshairs are
maxcosine = dhairs/sqrt(rhairs**2+dhairs**2) # if ray inside crosshairs, don't move
haircolor = color.black
roam = 0

# Decorate the front entrance slab
text(pos=(0, 0.77*h, R+d/2), text="No Exit", color=color.yellow,
           depth=0.3, height=0.7, align="center")

# Display extruded text
text( pos=(2.0,-0.3*sin(pi/10),-2.0), text='A', height=2.0, depth=0.5,
     color=(0,0,1.0), up=(0,cos(pi/3.4),-sin(pi/3.4)), axis=(0.5,0,1))
text( pos=(3.2,0,-2), text='B', height=2.0, depth=0.5,
     color=(1.0,1.0,0), axis=(1,0,0.3))
text( pos=(5.0,-0.6*sin(pi/18),-1.4), text='C', height=2.0, depth=0.5,
     color=(1.0,0,1.0), axis=(1,0,0.6), up=(0,cos(pi/8),sin(pi/8)) )

while True:
    # Toggle roam option
    if scene.mouse.events:
        m = scene.mouse.getevent()
        if m.press or m.drag:
            roam = True
        elif m.release or m.drop:
            roam = False

    # If in roaming mode, change center and forward according to mouse position
    if roam:
        ray = scene.mouse.ray
        if abs(dot(ray,scene.forward)) < maxcosine: # do something only if outside crosshairs
            newray = norm(vector(ray.x, 0, ray.z))
            angle = arcsin(dot(cross(scene.forward,newray),scene.up))
            newforward = rotate(scene.forward, axis=scene.up, angle=angle/30)
            scene.center = scene.mouse.camera+newforward*mag(scene.center-scene.mouse.camera)
            scene.forward = newforward
            scene.center = scene.center+scene.forward*ray.y/2.

    # Roll the log
    theta = theta + omega*dt
    log.x = log.x+v*dt
    log.rotate(angle=omega*dt)
    if log.x >= wide:
        v = -v0
        omega = -v/rlog
        if rightstop.color == color.red:
            rightstop.color = color.blue
        else:
            rightstop.color = color.red
    if log.x <= -wide:
        v = +v0
        omega = -v/rlog
        if leftstop.color == color.red:
            leftstop.color = color.blue
        else:
            leftstop.color = color.red

    # Move the cloud
    cloud.rotate(angle=omegacloud*dt, origin=(0,0,0), axis=(0,1,0))

    # Run the ball up and down
    ball.pos.y = ball.pos.y+vball*dt
    ball.rotate(angle=ballangle, axis=(0,1,0), origin=(0,0,0))
    if ball.pos.y >= y2:
        vball = -vball0
        ballangle = -ballangle
    if ball.pos.y <= y1:
        vball = +vball0
        ballangle = -ballangle

    # Move the smoke rings
    for i in range(Nrings):
        # Raise the smoke rings
        smoke[i].pos = smoke[i].pos+vector(0,dy,0)
        smoke[i].radius = smoke[i].radius+(dr/spacing)*dy
        smoke[i].thickness = smoke[i].thickness-(dthick/spacing)*dy
    y = y+dy
    if y >= spacing:
        # Move top ring to the bottom
        y = 0
        smoke[top].pos = (x0, y0, z0)
        smoke[top].radius = r0
        smoke[top].thickness = thick
        top = top-1
    if top < 0:
        top = Nrings-1

    # Update the analog clock on the back slab
    clock.update()
    
    rate(30)

