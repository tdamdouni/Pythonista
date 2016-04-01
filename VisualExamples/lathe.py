from visual import *

# Create a surface of revolution out of slices that are convex objects
# By David Scherer

def draw_slice(sweep, r, axis, frame, color):
    # comment in this line to see where the slices are:
    #color=(uniform(0,1),uniform(0,1),uniform(0,1))

    ls = len(sweep)
    pos = zeros( (len(r)*ls, 3), float64 )
    for j in range(len(r)):
        pos[j*ls:j*ls+ls] = sweep*r[j] + (axis[j],0,0)
    return convex(pos=pos,
                  frame = frame,
                  color = color,
                  )

def revolution(radius, length, slices=32, color = (1,1,1), pos = (0,0,0)):
    r = absolute(radius) # radius is a list of radii for all the slices

    # sweep = unit circle in the yz plane
    t = arange(0,2*pi,2*pi/slices)
    sweep = zeros( (slices,3), float64) # Numeric array (rows=slices)*(columns=3)
    sweep[:,1] = cos(t) # set middle column to cos(t)
    sweep[:,2] = sin(t) # set final column to sin(t)

    # axis[i] = center of the ith slice of the surface
    axis = arange(0,length,float(length)/len(r))

    group = frame(pos = pos)

    start = 0
    for i in range(1,len(r)-1):
        # if concave, show all convex slices up this point
        if (r[i+1] + r[i-1] - 2*r[i]) >= 0:  # have encountered concave region
            draw_slice(sweep,r[start:i],axis[start:i], group, color)
            start = i-1
    draw_slice(sweep,r[start:],axis[start:], group, color)

    return group

if __name__ == '__main__':
    scene.autocenter = True
    t = arange(0,1,0.02)
    s = revolution(sin(t*12.)*0.5 + 1.0, 5.0, pos=(3,0,0), color=color.red)
    s.axis = (0,1,0)

    glass = revolution( [0.5, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3, 0.4, 0.5],
                        length=5.0,
                        color=color.yellow)
    glass.axis = (0,1,0)
