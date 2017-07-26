# http://stackoverflow.com/questions/6304116/how-to-plot-a-3d-patch-collection-in-matplotlib

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch
from mpl_toolkits.mplot3d import Axes3D 
import mpl_toolkits.mplot3d.art3d as art3d


fig = plt.figure()
ax=fig.gca(projection='3d')

for i in ["x","y","z"]:
    circle = Circle((0, 0), 1)
    ax.add_patch(circle)
    art3d.pathpatch_2d_to_3d(circle, z=0, zdir=i)


ax.set_xlim3d(-2, 2)
ax.set_ylim3d(-2, 2)
ax.set_zlim3d(-2, 2)

plt.show()
