from __future__ import division
from visual import *
# Bruce Sherwood, August 2006
# Demonstration of transparency (opacity), materials, and local lights in Visual 5

# Create a texture to apply to a sphere to make a beach ball
bands = zeros([16,16,4], float)
for i in range(len(bands)):
    for j in range(len(bands[0])):
        op = 1
        if i % 2 == 0: # every other band is partially transparent
            op = 0.3
            col = color.cyan
        else:
            # choose a color for an opaque band of the beach ball:
            col = [color.blue, color.green, color.red,
                   color.yellow, color.cyan][i//2 % 5]
        bands[i][j] = (col[0], col[1], col[2], op)
stripes = materials.texture(data = bands,
                       mapping = "spherical",
                       interpolate = False)

scene.width = scene.height = 800
scene.forward = (-0.2,-0.2,-1)
width = 10 # of wood table
thick = 0.5 # thickness of wood
depth = 7 # of wood table
height = 2 # of side bars of table
xhit = height-thick # x distance of center of ball from side bar when it hits 
R = 2 # radius of ball
H = 10 # height of underside of ceiling above floor
L = 5 # length of pendulum to center of hanging lamp
# top of floor is at y=0 for convenience
scene.visible = False
floor = box(pos=(0,-thick/2,0), size=(width,thick,depth),
            shininess=0, color=color.orange, material=materials.wood)
left = box(pos=(-(width/2+thick/2),height/2-thick,0), size=(thick,height,depth),
            shininess=0, color=color.orange, material=materials.wood)
right = box(pos=(width/2+thick/2,height/2-thick,0), size=(thick,height,depth),
            shininess=0, color=color.orange, material=materials.wood)
back = box(pos=(0,height/2-thick,-(depth/2+thick/2)), size=(width+2*thick,height,thick),
            shininess=0, color=color.orange, material=materials.wood)
ceiling = box(pos=(0,H+thick/2,0), size=(width/10,thick,width/10), color=color.orange, material=materials.wood)
pendulum = frame(pos=(0,H,0), axis=(0,-1,0))
wire = curve(frame=pendulum, pos=[(0,0,0),(L,0,0)])
lamp = sphere(frame=pendulum, pos=(L,0,0), radius=0.03*L, color=color.white, material=materials.emissive)
sphere(pos=(0.1*width,R/4,0.45*depth), radius=R/4, color=color.red, material=materials.marble)
sphere(pos=(0.15*width,R/4,0.3*depth), radius=R/4, color=color.yellow, material=materials.marble)
sphere(pos=(0.15*width,R/4,-0.3*depth), radius=R/4, color=color.green, material=materials.marble)
sphere(pos=(0.1*width,R/4,-0.45*depth), radius=R/4, color=color.cyan, material=materials.marble)
scene.lights = []
scene.ambient = color.gray(0.25)
l1 = distant_light(direction=(6,2,4), color=color.gray(0.3))
l2 = distant_light(direction=(-10,2,4), color=color.gray(0.2))
lamplight = local_light(frame=pendulum, pos=(L,0,0), color=color.gray(0.5))
scene.center = (0,0.4*H,0)

ball = sphere(pos=(width/4,R,0), radius=R, up=(0,1,1), material=stripes)
xlimit = 0.5*width-R*sin(acos(1-(height-thick)/R))
v = vector(-0.5,0,0)
dt = 0.03
t = 0
scene.visible = True

while True:
    rate(100)
    ball.pos += v*dt
    ball.rotate(axis=(0,0,1), angle=-v.x*dt/R)
    if abs(ball.x) >= xlimit:
        v = -v
    angle = 0.02*cos(t)
    pendulum.rotate(axis=(1,0,0), angle=angle)
    t += dt
