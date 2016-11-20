# coding: utf-8

# https://forum.omz-software.com/topic/2431/possible-to-implement-latex-in-scene-module

import matplotlib.mathtext as mt
s=r'$\frac{A}{B} = C$'
mt.math_to_image(s, 'test.png')