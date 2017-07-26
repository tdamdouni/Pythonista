# http://stackoverflow.com/questions/11140163/python-matplotlib-plotting-a-3d-cube-a-sphere-and-a-vector

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")

#draw the arrow
ax.quiver(0,0,0,1,1,1,length=1.0)

plt.show()
