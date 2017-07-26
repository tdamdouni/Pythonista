# coding: utf-8

# https://github.com/shaun-h/pythonista-objc-utils/blob/master/AddKeyCommands.py

# author: Shaun Hevey
# This code has been taken and adapted from a number of scripts listed below.
# https://github.com/jsbain/objc_hacks/blob/master/keycommands.py
# https://github.com/jsbain/objc_hacks/blob/master/addnewfileshowchooser.py
# I need clean up this code 
from objc_util import *
import console
import time

c.method_setImplementation.restype = c_void_p
c.method_setImplementation.argtypes = [c_void_p, c_void_p]

c.method_getImplementation.restype = c_void_p
c.method_getImplementation.argtypes = [c_void_p]

def newTab(_cmd,_sel):
	vc=UIApplication.sharedApplication().keyWindow().delegate()
	dvc=vc.detailViewController()
	console.hide_output()
	time.sleep(0.1)
	dvc.addTab_(dvc.addTabButtonItem())

def closeTab(_cmd,_sel):
	vc=UIApplication.sharedApplication().keyWindow().delegate()
	dvc=vc.detailViewController()
	console.hide_output()
	time.sleep(0.1)
	dvc.closeSelectedTab_(None)

def handleCommandS(_cmd,_sel):
	vc=UIApplication.sharedApplication().keyWindow().delegate()
	console.hide_output()
	time.sleep(0.1)
	@on_main_thread
	def showChooser():
		vc.showMasterWithAnimationDuration_(0.3)
	@on_main_thread
	def hideChooser():
		vc.hideMasterWithAnimationDuration_(0.3)
	if vc.masterVisible():
		hideChooser()
	else:
		showChooser()

def handleCommandN(_self, _cmd):
	vc=UIApplication.sharedApplication().keyWindow().delegate()
	dvc=vc.detailViewController()
	console.hide_output()
	time.sleep(0.1)
	dvc.addTab_(dvc.addTabButtonItem())
	e=dvc.tabViewControllers()[-1]#newest added tab... maybe
	e.addNewFile_(e.addNewFileButton())

def addKeyCommandToPythonista(me, hint, key, modifier):
	app=ObjCClass('UIApplication').sharedApplication()
	UIKeyCommand=ObjCClass('UIKeyCommand')
	keycommands=list(app.keyCommands())
	CmdHHandler=create_objc_class('CmdHHandler',
											ObjCClass('UIResponder'),			
											[me])
											
	CmdHHandler_obj=CmdHHandler.new()
	aa = getattr(CmdHHandler_obj, me.__name__).method
	CmdHHandler_imp=c.method_getImplementation(aa)
	c.class_addMethod(UIApplication.ptr,sel(me.__name__),CmdHHandler_imp,'v@:')

	mykey=UIKeyCommand.keyCommandWithInput_modifierFlags_action_discoverabilityTitle_(key,modifier, sel(me.__name__),ns(hint))
	keycommands.append(mykey)
	__keycommands_obj=ns(keycommands)

	def replacement_keyCommands(_self,_cmd):
		return __keycommands_obj.ptr
	replacement=create_objc_class('replacement',ObjCClass('UIResponder'),	[replacement_keyCommands])
	replacement_obj=replacement.new()
	newimp=c.method_getImplementation(replacement_obj.keyCommands.method)
	oldimp=c.method_setImplementation(app.keyCommands.method,newimp)
	
if __name__ == '__main__':
	addKeyCommandToPythonista(handleCommandS, 'Show/Hide File Browser','s',1<<20)
	addKeyCommandToPythonista(handleCommandN, 'New File','n',1<<20)
	addKeyCommandToPythonista(newTab, 'New Tab','t',1<<20)
	addKeyCommandToPythonista(closeTab, 'Close Tab','m',1<<20)
