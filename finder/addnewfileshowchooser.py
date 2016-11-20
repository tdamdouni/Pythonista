# coding: utf-8

# https://github.com/jsbain/objc_hacks/blob/master/addnewfileshowchooser.py

from objc_util import *
import console,time

vc=UIApplication.sharedApplication().keyWindow().delegate()
dvc=vc.detailViewController()

@on_main_thread
def _addTab():
	dvc.addTab_(dvc.addTabButtonItem())
	
@on_main_thread
def _addNewFile():
	e=dvc.tabViewControllers()[-1]#newest added tab... maybe
	e.addNewFile_(e.addNewFileButton())
	
def show_file_chooser_panel(newTab=False):
	console.hide_output()
	if newTab:
		_addTab()
	time.sleep(0.1)
	@on_main_thread
	def showChooser():
		vc.showMasterWithAnimationDuration_(0.3)
	showChooser()
	
def add_new_file():
	console.hide_output()
	time.sleep(0.1)
	_addTab()
	_addNewFile()

