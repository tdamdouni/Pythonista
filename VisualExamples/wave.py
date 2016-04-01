from visual import *

# David Scherer

dt = 0.1

g = []
for i in range(3):
  g.append(display(x = 0, y = 30 + 200*i, width=600, height=170))

g[0].title="k=6N/m mass=2.0kg"
g[1].title="k=6N/m mass=1.0kg"
g[2].title="k=6N/m mass=0.5kg"

bands = [ curve( x = arange(-50,50), display=g[0], color=color.red, k = 6., mass = 2.0),
          curve( x = arange(-50,50), display=g[1], color=color.yellow, k = 6., mass = 1.0),
          curve( x = arange(-50,50), display=g[2], color=color.green, k = 6., mass = 0.5),
        ]

for band in bands:
    band.radius = 0.5
    band.momentum = zeros((100,3),float)

    ### Uncomment exactly one of the following lines: ###

    band.momentum[:25,1] = sin(band.x[:25]*pi / 25.0)*3   # half-wave pulse
##    band.momentum[:25,1] = sin(band.x[:25]*2*pi / 25.0)*5 # full-wave pulse
##    band.momentum[:25,0] = sin(band.x[:25]*pi / 25.0)*5   # compression wave
##    band.momentum[:,1] = sin(band.x * 4 * pi / 100.0)*2   # standing wave
##    band.momentum[25,1] = 20                             # single point impulse (messy)

while True:
    rate(100)
    for band in bands:
        # Keep endpoints fixed:
        band.momentum[0] = band.momentum[-1] = vector(0,0,0)

        # Integrate velocity:
        band.pos = band.pos + (band.momentum/band.mass*dt)

        # force[n] is the force on point n from point n+1 (to the right):
        force = band.k * (band.pos[1:] - band.pos[:-1])

        # all points but the last experience forces to the right:
        band.momentum[:-1] = band.momentum[:-1] + force * dt

        # all points but the first experience forces to the left:
        band.momentum[1:] = band.momentum[1:] - force * dt
