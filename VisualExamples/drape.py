from visual import *

print("""
Click to place spheres under falling string.
Right button drag to rotate view.
  On a one-button mouse, right is Command + mouse.
Middle button drag up or down to zoom in or out.
  On a two-button mouse, middle is left + right.
  On a one-button mouse, middle is Option + mouse.
""")

# David Scherer

scene.title = "Drape"
restlength = 0.02
m = 0.010 * restlength
g = 9.8
dt = 0.002
k = 3
damp = (1-0)**dt
nspheres = 3
floor = 0

# Create the stringy thing:
band = curve( x = arange(-1,1,restlength), 
              y = 1,
              radius = 0.02
            )

band.p = band.pos * 0

##scene.range = 1.5
##scene.autoscale = 0

# Let the user position obstacles:
spheres = []
for i in range(nspheres):   
    s = sphere( pos = scene.mouse.getclick().pos,  #(i*0.6 - 0.7,0.5 + i*0.1,0),
                radius = 0.25, 
                color = (abs(sin(i)),cos(i)**2,(i%10)/10.0) )
    spheres.append( s )

while True:
  rate(1.0 / dt)

  if scene.mouse.clicked:
    i = len(spheres)
    s = sphere( pos = scene.mouse.getclick().pos,
                radius = 0.25, 
                color = (abs(sin(i)),cos(i)**2,(i%10)/10.0) )
    spheres.append( s )

  if floor:
    below = less(band.pos[:,1],-1)
    band.p[:,1] = where( below, 0, band.p[:,1] )
    band.pos[:,1] = where( below, -1, band.pos[:,1] )

  # need a more physical way to make 'damped springs' than this!
  band.p = band.p * damp

  #band.p[0] = 0   # nail down left endpoint
  #band.p[-1] = 0  # nail down right endpoint

  band.pos = band.pos + band.p/m*dt

  #gravity
  band.p[:,1] = band.p[:,1] - m * g * dt

  # force[n] is the force on point n from point n+1 (to the right):
  length = (band.pos[1:] - band.pos[:-1])
  dist = sqrt(sum(length*length,-1))
  force = k * ( dist - restlength )
  force = length/dist[:,newaxis] * force[:,newaxis]

  band.p[:-1] = band.p[:-1] + force*dt
  band.p[1:] = band.p[1:] - force*dt

  # color based on "stretch":  blue -> white -> red
  c = clip( dist/restlength * 0.5, 0, 2 )

  #   blue (compressed) -> white (relaxed) -> red (tension)
  band.red[1:] = where( less(c,1), c, 1 )
  band.green[1:] = where( less(c,1), c, 2-c )
  band.blue[1:] = where( less(c,1), 1, 2-c )

  for s in spheres:
    dist = mag( band.pos - s.pos )[:,newaxis]
    inside = less( dist, s.radius )
    if sometrue(inside):
        R = ( band.pos - s.pos ) / dist
        surface = s.pos + (s.radius)*R

        band.pos = surface*inside + band.pos*(1-inside)

        pdotR = sum(asarray(band.p)*asarray(R),-1)
        band.p = band.p - R*pdotR[:,newaxis]*inside
