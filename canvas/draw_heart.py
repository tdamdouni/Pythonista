# -*- coding: utf-8 -*-
# draw_heart.py -- draw a heart on the Pythonista canvas
# http://gaming.jhu.edu/~phf/2012/fall/cs112/assignment-02.pdf or
# https://plus.google.com/app/basic/stream/z12lunmjbx33vh5bt04cilrpelnzcbhoorg0k

'''
Try commenting out the draw_path() line below.
How do I fill just the inner part of the path?
'''

import canvas, math, sys

def draw_heart(scale = 18):  # 18 = full canvas
    #print(scale)  # useful for debugging
    first_time = True
    (xorigin, yorigin) = canvas.get_size()
    xorigin *= 0.5    # in the center
    yorigin *= 0.588  # north of center
    detail = 100
    canvas.begin_path()
    for t in xrange(int(2 * math.pi * detail)):
        t *= detail
        x = scale * (16 * math.sin(t) ** 3)
        y = scale * (13 * math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4 * t))
        if first_time:  # hide the seams
            canvas.move_to(x + xorigin, y + yorigin)
            first_time = False
        canvas.add_line(x + xorigin, y + yorigin)
    canvas.set_line_width(1)
    canvas.close_path()
    canvas.draw_path()  # try commenting out this line...
    canvas.set_fill_color(1, 0, 0)
    canvas.fill_path()  # how do I fill just the inner part?

print('Starting...')
w = 600
h = w * 0.875
canvas.set_size(w, h)
canvas.add_rect(0, 0, w, h)
draw_heart(18)

#for i in xrange(2, 19, 4):
#    draw_heart(i)
