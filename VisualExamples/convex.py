from visual import *
from random import uniform

# David Scherer

scene.range = 3

a = convex(color=(0.5,0,0))
b = convex(color=(0,0.5,0))
c = convex(color=(0,0,0.5))
d = convex(color=(0.5,0,0.5))
e = convex(color=(0.5,0.5,0))
f = convex(color=(0,0.5,0.5))

# circle
t = arange(0,2*pi,0.1)
e.pos = transpose( (sin(t), cos(t)+2, 0*t) )

# triangle
t = arange(0,2*pi,2*pi/3)
f.pos = transpose( (sin(t)-2, cos(t)+2, 0*t) )

# disk
for t in arange(0,2*pi,0.1):
    a.append(pos = (cos(t),0,sin(t)))
    a.append(pos = (cos(t),0.2,sin(t)))

# box
for i in range(8):
    p = vector((i/4)%2 - 2.5, (i/2)%2 - 0.5, (i)%2 - 0.5)
    b.append(pos=p)

# random sphere
L = []
for i in range(1000):
    L.append(vector(2,0) + norm(vector(uniform(-1,1),uniform(-1,1),uniform(-1,1))))
c.pos = L

# lat/long sphere
L = []
for t in arange(0,2*pi,0.2):
    for s in arange(0,pi,0.1):
        L.append((cos(t)*sin(s)+2, sin(t)*sin(s)+2, cos(s)))
d.pos = L

# modify the disk
p = a
p.color = (p.color[0]*2, p.color[1]*2, p.color[2]*2)
while 1:
    rate(10)
    if scene.mouse.clicked:
        c = scene.mouse.getclick()
        p.append(pos=c.pos)
    p.pos[-1] = scene.mouse.pos
