#!python2

# http://stackoverflow.com/questions/24123659/scatter-plot-3d-with-labels-and-spheres

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def drawSphere(xCenter, yCenter, zCenter, r):
    #draw sphere
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x=np.cos(u)*np.sin(v)
    y=np.sin(u)*np.sin(v)
    z=np.cos(v)
    # shift and scale sphere
    x = r*x + xCenter
    y = r*y + yCenter
    z = r*z + zCenter
    return (x,y,z)


x = 10*np.random.rand(20)
y = 10*np.random.rand(20)
z = 10*np.random.rand(20)
r = np.random.rand(20)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# draw a sphere for each data point
for (xi,yi,zi,ri) in zip(x,y,z,r):
    (xs,ys,zs) = drawSphere(xi,yi,zi,ri)
    ax.plot_wireframe(xs, ys, zs, color="r")


plt.show()
