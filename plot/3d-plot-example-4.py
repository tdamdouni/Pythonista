# https://gist.github.com/Serpens/18e313bc43ebf3d796c2

import pylab
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d

fig=pylab.figure()
ax = mpl_toolkits.mplot3d.axes3d.Axes3D(fig)
for i in xrange(len(array)):
    ax.plot([i] * 512, numpy.arange(0, 512), zs=array[i])
pylab.show()
