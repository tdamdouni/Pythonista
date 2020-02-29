# coding: utf-8

# https://forum.omz-software.com/topic/2014/beta-tinkering-with-pythonista-s-internals-using-objc_util/11

# UIView has a built-in recursiveDescription method that produces a tree-like representation of all subviews.

from __future__ import print_function
from objc_util import *
w=ObjCClass('UIApplication').sharedApplication().keyWindow()
main_view=w.rootViewController().view()

def filter_subviews(view,text=None, objcclasstext=None):
	matching_svs=[]
	sv=view.subviews()
	if sv is None:
		return matching_svs
	for v in sv:
		if objcclasstext and objcclasstext in v._get_objc_classname():
			matching_svs.append(v)
		if text and hasattr(v,'text'):
			if str(v.text()) and text in str(v.text()):
				matching_svs.append(v)
		matching_svs.extend(
		filter_subviews(v, text=text, objcclasstext=objcclasstext))
	return matching_svs
	
# don't find editor window, so concatenate string
print('find'+'me')
# in this case, only one entry will be returned.  otherwise, may need to look at list to figure out which view is the one you are seeking.
console_view=filter_subviews(main_view,'find'+'me')[0]

