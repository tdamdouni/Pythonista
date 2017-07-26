# http://stackoverflow.com/questions/6870922/how-to-plot-a-data-cube-in-python

import random
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

mypoints = []
for _ in range(100):
	mypoints.append([random.random(),    #x
	random.random(),     #y
	random.random(),     #z
	random.randint(10,100)]) #scalar
	
data = zip(*mypoints)

fig = pyplot.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(data[0], data[1], data[2], c=data[3])
pyplot.show()

