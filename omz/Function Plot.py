# MPL Plot
# A simple demo of using matplotlib in Pythonista.

import console
console.clear()
print 'Loading NumPy...'
import numpy
print 'Loading matplotlib...'
import matplotlib.pyplot as plt
import math

print 'Plotting...'
plt.grid(True)
plt.title('matplotlib Demo')
x = numpy.linspace(0.0, 2 * math.pi)
p1 = plt.plot(x, numpy.sin(x), lw=2, c='r')
p2 = plt.plot(x, numpy.cos(x), lw=2, c='b')
plt.legend([p1[0], p2[0]], ['sin(x)', 'cos(x)'], loc=4)
plt.show()

print 'Tip: You can tap and hold the image to save it to your photo library.'