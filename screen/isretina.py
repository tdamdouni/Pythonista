from __future__ import print_function
# https://gist.github.com/xen/01c913b4b13759e035880f74dcaa3f8f

from objc_util import *
us = ObjCClass('UIScreen')
if us.mainScreen().scale() == 2.0:
	print('Retina')
elif us.mainScreen().scale() == 3.0:
	print('iPhone 6 Plus')
else:
	print('Non retina')

