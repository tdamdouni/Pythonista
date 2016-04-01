from __future__ import division
from visual.graph import *

# Bruce Sherwood, Jan. 1, 2008
# Use points object to make a pixel-like plot of a fractal

XMIN = -2
XMAX = 0.5
YMIN = -1
YMAX = 1
g = gdisplay(width=750, height=600, xmin=XMIN, xmax=XMAX, ymin=YMIN, ymax=YMAX)
pixels = gdots(shape='square', size=2)
# Scale factor: 2 units (YMAX-YMIN) equals 600 screen pixels
# Plot 2 by 2 gdots points 2*(2units/600pixels) apart:
r = 2*2/600

# Mandelbrot set (see Wikipedia, for example):
max_iteration = 100
for y0 in arange(YMIN, YMAX, r): # range over all pixel positions
    for x0 in arange(XMIN, XMAX, r):
        z = z0 = complex(x0,y0)
        iteration = 0
        while ( abs(z) < 2 and iteration < max_iteration):
            z = z*z+z0
            iteration += 1
        # Leave points black if the iteration quickly escapes:
        if (.1 < iteration/max_iteration < 1):
            c = color.hsv_to_rgb((iteration/max_iteration-.1,1,1))
            pixels.plot(pos=(x0,y0), color=c)

