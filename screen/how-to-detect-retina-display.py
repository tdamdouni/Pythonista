from __future__ import print_function
# https://forum.omz-software.com/topic/3251/how-to-detect-retina-display

# isretina.py
from objc_util import *
us = ObjCClass('UIScreen')
if us.mainScreen().scale() == 2.0:
	print('Retina')
elif us.mainScreen().scale() == 3.0:
	print('iPhone Plus')
else:
	print('Non retina')
	
# --------------------

from objc_util import ObjCClass
scale = ObjCClass('UIScreen').mainScreen().scale()
print({2: 'Retina', 3: 'iPhone Plus'}.get(scale, 'Non retina'))

# --------------------

