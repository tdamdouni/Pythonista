from visual import *

print("""
Right button drag to rotate "camera" to view scene.
  On a one-button mouse, right is Command + mouse.
Middle button to drag up or down to zoom in or out.
  On a two-button mouse, middle is left + right.
  On a one-button mouse, middle is Option + mouse.
""")
scene.title = "Lorenz differential equation"
scene.center = vector(25,0,0)

lorenz = curve( color = color.black, radius=0.3 )

# Draw grid
for x in arange(0,51,10):
    box(pos=(x,0,0), axis=(0,0,50), height=0.4, width=0.4, color=(0.6,0.6,0.6) )
for z in arange(-25,26,10):
    box(pos=(25,0,z), axis=(50,0,0), height=0.4, width=0., color=(0.6,0.6,0.6) )

dt = 0.01
y = vector(35, -10, -7)

for t in arange(0,10,dt):
  # Integrate a funny differential equation
  dydt = vector( - 8.0/3*y[0]           + y[1]*y[2],
                              - 10*y[1] +   10*y[2],
                 -  y[1]*y[0] + 28*y[1] -      y[2] );
  y = y + dydt*dt

  # Draw lines colored by speed
  c = clip( [mag(dydt) * 0.005], 0, 1 )[0]

  lorenz.append( pos=y, color=(c,0, 1-c) )

  rate( 500 )
