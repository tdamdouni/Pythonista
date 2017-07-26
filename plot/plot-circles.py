# http://stackoverflow.com/questions/6304116/how-to-plot-a-3d-patch-collection-in-matplotlib

import matplotlib
import matplotlib.pyplot as P
import mpl_toolkits.mplot3d as M3

fig = P.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
circles = matplotlib.collections.PatchCollection(
    [matplotlib.patches.Circle((0, 0), 1) for count in range(3)],
    offsets=(0, 0))
M3.art3d.patch_collection_2d_to_3d(circles, zs=[0], zdir='z')
ax.add_collection(circles)
P.show()
