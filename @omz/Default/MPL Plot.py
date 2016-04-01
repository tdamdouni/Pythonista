# MPL Plot
# A simple demo of using matplotlib in Pythonista.

import console
console.clear()
print 'Generating plot... (this may take a little while)'

import numpy
import matplotlib.pyplot as plt
import math

plt.grid(True)
plt.title('matplotlib Demo')
x = numpy.linspace(0.0, 2 * math.pi)
p1 = plt.plot(x, numpy.sin(x), lw=2, c='r')
p2 = plt.plot(x, numpy.cos(x), lw=2, c='b')
plt.legend([p1[0], p2[0]], ['sin(x)', 'cos(x)'], loc=4)
plt.show()

print 'Tip: You can tap and hold the image to save it to your photo library.'
