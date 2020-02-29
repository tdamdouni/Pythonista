# coding: utf-8

# https://forum.omz-software.com/topic/2371/sub-views-of-navigationview-are-not-accessible

from __future__ import print_function
with open('file.pyui','r') as f:
	print(f.read())
	
#==============================

def get_navigationview_root(nv):
	o=[v for v in gc.get_objects() if hasattr(v,'navigation_view') and v.navigation_view==nv and not v.superview]
	return o[0]

