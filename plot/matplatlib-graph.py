# https://forum.omz-software.com/topic/3421/what-is-wrong-with-this-code/3

# The first step is to import the required packages. The aliases `plt` and
# `np` are coding conventions.
# * `Axes3D` allows adding 3d objects to a 2d matplotlib plot.
# * The `pyplot` submodule from the **matplotlib** library, a python 2D
# plotting library which produces publication quality figures.
# * The `numpy` library for efficient numeric-array manipulation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

# Now we set up the data to plot, the `x`, `y` and `z` arrays are the
# coordinates for the start points of each arrow, whilst the `u`, `v` and
# `w` arrays are the coordinates of the endpoints.
x, y, z = np.meshgrid(np.arange(-0.8, 1, 0.2),
                      np.arange(-0.8, 1, 0.2),
                      np.arange(-0.8, 1, 0.8))

u = np.sin(np.pi * x) * np.cos(np.pi * y) * np.cos(np.pi * z)
v = -np.cos(np.pi * x) * np.sin(np.pi * y) * np.cos(np.pi * z)
w = (np.sqrt(2.0 / 3.0) * np.cos(np.pi * x) * np.cos(np.pi * y) *
     np.sin(np.pi * z))

# Now we create the plot with `quiver()`. The 1.4.x version of newer of the
# **matplotlib** library is required for this command to work. For the colour
# of the arrows it is possible to use either html hexadecimal codes, html
# colour names or a 3-tuple of rgb values.
fig = plt.figure()
ax = fig.gca(projection='3d')

ax.quiver(x, y, z, u, v, w,                 # data
          length=0.15,                      # arrow length
          color='Tomato'                 # arrow colour
          )

ax.set_title('3D Vector Field')             # title
ax.view_init(elev=18, azim=30)              # camera elevation and angle
ax.dist=8                                   # camera distance

plt.show()

