# http://toolbox.pep-dortmund.org/files/archive/2013/Matplotlib.html

import matplotlib
import matplotlib.pyplot as plt
from pylab import *

r = linspace(0, 10, 1000)
#r = linspace(0, 10, 50)
theta = 2 * pi * r

polar(theta, r)
plt.plot(theta, r)
plt.show()
