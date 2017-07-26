#!python2

# http://stackoverflow.com/questions/24123659/scatter-plot-3d-with-labels-and-spheres

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

x = np.random.rand(20)
y = np.random.rand(20)
z = np.random.rand(20)
r = np.random.rand(20)


plt.rc('text', usetex=True)
plt.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x, y, z, s=np.pi*r**2*100, c='blue', alpha=0.75)

ax.set_xlabel(r'$x$ $\left[\frac{\text{Mpc}}{h}\right]$')
ax.set_ylabel(r'$y$ $\left[\frac{\text{Mpc}}{h}\right]$')
ax.set_zlabel(r'$z$ $\left[\frac{\text{Mpc}}{h}\right]$')

#plt.savefig('spheres.png')

plt.show()
