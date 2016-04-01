from visual import *
from random import uniform, randint

scene.forward = (-0.25,-0.25,-1)

nboxes = 8
nlinks = 16
maxgrid = 10

# Create some random cylinders:
nodes = []
for t in arange(-pi,pi,2*pi/nboxes):
  b = cylinder( pos=(10*sin(t),0,10*cos(t)) )
  b.color = b.icolor = (0.5,0.5,1)
  height = uniform(0.5,4)
  b.axis = (0,height,0)
  nodes.append( b )

# Create some random links:
links = []
for l in range(nlinks):
  i = randint(0,nboxes-1)
  j = randint(0,nboxes-1)
  c = curve( ends=[nodes[i].pos,nodes[j].pos], radius=0.2 )
  c.red = 0
  c.green = uniform(0.3,1)
  c.blue = 0
  c.pos = c.ends
  links.append(c)

# Draw a grid:
for i in range(maxgrid+1):
    curve(pos=[(2*i-maxgrid,0,-maxgrid),(2*i-maxgrid,0,maxgrid)], color=color.cyan)       
    curve(pos=[(-maxgrid,0,2*i-maxgrid),(maxgrid,0,2*i-maxgrid)], color=color.cyan)
box(pos=(0,-0.6,0),width=2*maxgrid,length=2*maxgrid,height=1,color=(0,0,0.1))

# Drag and drop loop
drag = None
while True:
  rate(100)
  if scene.mouse.events:
    c = scene.mouse.getevent()
    if drag and (c.drop or c.click):   # drop the selected object
      newpos = c.project(normal=scene.up, d=yoffset)+offset
      if abs(newpos.x)<=maxgrid and abs(newpos.z)<=maxgrid:
        drag.pos = newpos
      drag.color = drag.icolor
      drag = None
    elif c.pick and hasattr(c.pick,"icolor"):   # pick up the object
      drag = c.pick
      drag.color = color.white
      yoffset = c.pickpos.y
      offset = drag.pos-c.project(normal=scene.up, d=yoffset)
  if drag:
    newpos = scene.mouse.project(normal=scene.up, d=yoffset)+offset
    if abs(newpos.x)<=maxgrid and abs(newpos.z)<=maxgrid:
      drag.pos = newpos
  
  for lnk in links: lnk.pos = lnk.ends
