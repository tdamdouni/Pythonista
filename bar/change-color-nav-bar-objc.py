# https://gist.github.com/jsbain/a74e256d3972192f3d70b9bc1bcbe1bc

from objc_util import *
import ui
def find_nav_bar(v):
	'''traverse up super views unil a nav bar is found, or return None'''
	sv=v.superview()
	if sv:
		for c in sv.subviews():
			if c._get_objc_classname()==b'UINavigationBar':
				return c
		return find_nav_bar(sv)
@on_main_thread
def cycle_color(sender):
	V=ObjCInstance(v)
	navbar=find_nav_bar(V)
	if navbar:
		oldcolor=navbar._backgroundView().backgroundColor()
		r=(oldcolor.red()-1/53)%1
		g=(oldcolor.green()-1/13)%1.
		b=(oldcolor.blue()-1/27)%1.
		newcolor=UIColor.colorWithRed_green_blue_alpha_(r,g,b,1.)
		navbar._backgroundView().backgroundColor=newcolor
v=ui.View(frame=(0,0,333,500),bg_color='white')
b=ui.Button(title='Push Me',frame=(50,50,100,100))
b.action=cycle_color
v.add_subview(b)
v.present('sheet')
n=find_nav_bar(ObjCInstance(v))

