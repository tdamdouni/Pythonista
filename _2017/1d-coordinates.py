# https://forum.omz-software.com/topic/4031/1d-coordinates/8

import numpy
from matplotlib import pyplot

#100 linear samples between -10 and 10
x = numpy.linspace(-10, 10, 100)
#draw a red line through f(x) = x
pyplot.plot(x, x, 'r-')
#draw a blue dotted line through f(x) = sin(x)
pyplot.plot(x, numpy.sin(x), 'b--')
#show the plot
pyplot.show()