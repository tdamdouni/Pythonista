# coding: utf-8

# https://forum.omz-software.com/topic/2845/request-for-an-app/11

from __future__ import print_function
from PIL import Image
import photos

im = photos.pick_image() # Load the image with whatever method you'd like

dimension = 1 if raw_input("Which dimension are you inputting?\n").lower() == "width" else 0

dimension_value = int(raw_input("Value: "))

"""
We can use the proportion:

image_width       your_width
------------ = -----------------
image_height   unknown_dimension

and with this, cross-multiply"""

if dimension: # We're solving for the height
    print(im.size[1]*dimension_value / float(im.size[0]))
else:
    print(im.size[0]*dimension_value / float(im.size[1]))
