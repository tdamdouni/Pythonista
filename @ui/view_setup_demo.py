# coding: utf-8

# https://gist.github.com/jsbain/9ad6220833b3ee0097e2

import ui,time

def setup_view(v):
	''' a very slow and complicated setup'''
	for i in xrange(10):
		b=ui.Button(bg_color=(1,i/20.,0))
		b.frame=(200,0,50,50)
		b.y=i*50
		v.add_subview(b)
		time.sleep(0.2)
def show_activity_indicator(v):
	a=ui.ActivityIndicator(name='activity')
	a.center=v.bounds.center()
	a.start_animating()
	v.add_subview(a)
def remove_activity_indicator(v):
	v.remove_subview(v['activity'])
	
def method0():
	'''simple, slow, ugly, subviews are visible adding one at a time'''
	v=ui.View(bg_color=(1,1,1),frame=(0,0,700,700))
	v.present('sheet')
	setup_view(v)
	
def method1():
	'''show an activity indicator while waiting'''
	v=ui.View(bg_color=(1,1,1),frame=(0,0,700,700))
	v.present('sheet')
	show_activity_indicator(v)
	def setup():
		setup_view(v)
	ui.delay(setup,0)
	remove_activity_indicator(v)
	
def method2():
	'''hide the view'''
	v=ui.View(bg_color=(1,1,1),frame=(0,0,700,700))
	v.hidden=True
	v.present('sheet')
	setup_view(v)
	v.hidden=False
	
def method3():
	'''use a root view, so you can show some stuff, like bgcolor, or activity indicator but hide this component until setup'''
	root=ui.View(bg_color=(1,1,1),frame=(0,0,700,700))
	show_activity_indicator(root)
	v=ui.View(frame=root.bounds,flex='wh')
	root.add_subview(v)
	v.hidden=True
	root.present('sheet')
	setup_view(v)
	v.hidden=False
	remove_activity_indicator(root)
import dialogs
def show_menu():
	choices={'0: basic approach   ':method0,'1: activity indicator   ':method1,'2: hidden root     ':method2,'3: hidden subview/activity indicator':method3}
	choice=dialogs.list_dialog('select setup method',choices.keys())
	choices[choice]()
show_menu()