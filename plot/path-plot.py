# http://stackoverflow.com/questions/27475626/is-there-a-way-to-draw-3d-lines-as-a-series-of-circles-with-matplotlib

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d
import numpy as np
x = np.linspace(0, 6, 10)
y = np.sin(x)
z = x

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')

ax.plot(x, y, z
         , linestyle='-'
         , linewidth=20
         , marker='o'
         , markersize=20
         , solid_capstyle='round'
)
ax.set_xlim3d(-1, 7)
ax.set_ylim3d(-2, 2)
ax.set_zlim3d(-1, 7)
plt.show()

