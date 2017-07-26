# coding: utf-8

# https://github.com/jsbain/objc_hacks/blob/master/apphack.py

''' A set of tools to add or delete custom buttons from the toolbar.  This may not be super robust, but seems to work ok.  Button objects and actions are saved so they survive global clearing, but thid has not been tested extensively.  If a function relies on imports that occured outside of the function, these might dissappear -- user must make sure those modules are added to a module that is kept by pythonista, such as anything in site-packages, or name starting with __   '''

from objc_util import *
import ui,console
import weakref
from functools import partial


w=ObjCClass('UIApplication').sharedApplication().keyWindow()
main_view=w.rootViewController().view()

def get_toolbar(view):
	#get main editor toolbar, by recursively walking the view
	sv=view.subviews()
	
	for v in sv:
		if v._get_objc_classname()=='OMTabViewToolbar':
			return v
		tb= get_toolbar(v)
		if tb:
			return tb
def create_toolbar_button(action,image,index=0,tag=''):
	'''create a button on main toolbar, with action,imagename, index location, and string tagname.  button and action are stored in __persistent_views[index].  tag allows finding view using tb.viewFromTag_(hash(tag)) (old idea)'''
	assert(callable(action))
	
	tb=get_toolbar(main_view)
	global __persistent_views
	try:
		__persistent_views
	except NameError:
		__persistent_views={}
	#check for existing button in this index and delete if needed
	remove_toolbar_button(index)
	
	#add new button to the left of the rightbuttons.  index 0 is next to left buttons, index 1 is further left, etc
	#store so it is not cleared.
	
	btn=ui.Button( frame=(tb.size().width -
	tb.rightItemsWidth()-(index+1)*40,22,40,40))
	btn.flex='L'
	btn.image=ui.Image.named(image)
	btn.action=action
	btn_obj=ObjCInstance(btn)
	btn_obj.tag=hash(tag)
	__persistent_views[index]=(btn,action,tag)
	tb.addSubview_(btn_obj)
	return btn
def remove_toolbar_button(index):
	global __persistent_views
	try:
		btn,action,tag=__persistent_views.pop(index)
		btn.action= None
		ObjCInstance(btn).removeFromSuperview()
	except KeyError:
		pass
		
if __name__=='__main__':
	def run_script(sender):
		'''run a script without clearing glbals'''
		import editor
		editor.reload_files()
		execfile(editor.get_path(),globals())
		
	create_toolbar_button(run_script,'iow:play_32',0,'execfile')

