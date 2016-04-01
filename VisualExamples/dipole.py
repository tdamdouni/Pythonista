from visual import *

print("""
Click to plot a normalized electric field vector.
Vectors are blue if low magnitude, red if high.
Right button drag to rotate camera to view scene.
  On a one-button mouse, right is Command + mouse.
Middle button drag up or down to zoom in or out.
  On a two-button mouse, middle is left + right.
  On a one-button mouse, middle is Option + mouse.
""")

ec = 1.6e-19  # electron charge

scene.title="Electric Field Vectors"
scene.range = 2e-13

charges = [ sphere( pos = (-1e-13,0,0), Q =  ec, color=color.red, radius = 6e-15 ),
            sphere( pos = ( 1e-13,0,0), Q = -ec, color=color.blue, radius = 6e-15 ),
          ]

def getfield(p):
    f = vector(0,0,0)
    for c in charges:
        f = f + (p-c.pos) * 8.988e9 * c.Q / mag(p-c.pos)**3
    return f

while True:
    p = scene.mouse.getclick().pos
    f = getfield(p)
    m = mag(f)
    red = maximum( 1-1e17/m, 0 )
    blue = minimum(   1e17/m, 1 )
    if red >= blue:
        blue = blue/red
        red = 1.0
    else:
        red = red/blue
        blue = 1.0
    arrow( pos=p, axis=f * (4e-14/1e17),
           shaftwidth = 6e-15,
           color=(red,0,blue))
