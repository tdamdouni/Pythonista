from visual import *

# Mikhail Temkine, University of Toronto, April 2007

print("""
Box lighting test
""")

r = 3
a1 = a2 = a3 = 0.0

arrow(pos=(0, 4, 0), axis=(0, 1, 0), color=color.red)
boxy = box(size=(3,3,3), color=(0.5, 0.5, 0.5), material=materials.rough)
b1 = sphere(radius=0.3, pos=(r, 0, 0),
            color=color.magenta, material=materials.emissive)
b2 = sphere(radius=0.3, pos=(0, 0, r),
            color=color.yellow, material=materials.emissive)
b3 = arrow(radius=0.3, pos=(0, 0, r),
            color=color.green, material=materials.emissive)
l1 = local_light(pos=b1.pos, color=b1.color)
l2 = local_light(pos=b2.pos, color=b2.color)
l3 = distant_light(direction=b3.pos, color=b3.color)

while True:
    rate(100)
    l1.pos = b1.pos = r*vector(cos(a1), sin(a1), b1.z)
    a1 += 0.02
    l2.pos = b2.pos = (r+0.4)*vector(b2.x, sin(a2), cos(a2))
    a2 += 0.055
    l3.direction = b3.pos = (r+3)*vector(sin(a3), b3.y, cos(a3))
    b3.axis = b3.pos * -0.3
    a3 += 0.033
    
