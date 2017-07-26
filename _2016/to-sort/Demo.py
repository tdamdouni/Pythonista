# coding: utf-8

#!/usr/bin/env python3

# Copyright (c) 2016 Lukas Kollmer <lukas@kollmer.me>

# https://gist.github.com/lukaskollmer/859d2e3cb8d026d5bb44b87431330ad9

'''
Purpose: Showcases a crash when calling a nonexistent python method from within an Objective-C method
'''
import console
from objc_util import *


console.clear()

UITableViewController = ObjCClass('UITableViewController')
UIViewController = ObjCClass('UIViewController')
UITableView = ObjCClass('UITableView')
UITableViewCell = ObjCClass('UITableViewCell')
UIColor = ObjCClass('UIColor')
UINavigationController = ObjCClass('UINavigationController')
UIBarButtonItem = ObjCClass('UIBarButtonItem')



def tableView_numberOfRowsInSection_(_self, _cmd, _tv, section):
	return 1

tableView_numberOfRowsInSection_.encoding = 'q0@0:0@0@0'
tableView_numberOfRowsInSection_.restype = c_long


def tableView_heightForRowAtIndexPath_(_self, _cmd, _tv, _ip):
	return float(30)

def tableView_cellForRowAtIndexPath_(_self, _cmd, _tv, _ip):
	cell = UITableViewCell.alloc().initWithStyle_reuseIdentifier_(1, 'Cell')
	python_method_that_does_not_exist()
	return cell.ptr
	
tableView_cellForRowAtIndexPath_.encoding = '@0@0:0@0@0'



def dismiss(_self, _cmd):
	vc = ObjCInstance(_self)
	vc.dismissViewControllerAnimated_completion_(True, None)

	
@on_main_thread
def main():
	rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
	tabVC = rootVC.detailViewController()
	methods = [tableView_numberOfRowsInSection_, tableView_cellForRowAtIndexPath_, dismiss]
	protocols = ['UITableViewDataSource', 'UITableViewDelegate']
	CustomViewController = create_objc_class('CustomViewController', UIViewController, methods=methods, protocols=protocols)
	vc = CustomViewController.new().autorelease()
	vc.title = 'Title'
	table_view = UITableView.alloc().initWithFrame_style_(((0, 0), (0, 0)), 0)
	table_view.setDataSource_(vc)
	table_view.setDelegate_(vc)
	vc.view = table_view
	
	closeButton = UIBarButtonItem.alloc().initWithBarButtonSystemItem_target_action_(0, vc, sel('dismiss'))
	vc.navigationItem().setLeftBarButtonItem_(closeButton)
	
	navController = UINavigationController.alloc().initWithRootViewController_(vc)
	vc.setModalPresentationStyle_(2) #2 for sheet, 0 for full screen
	navController.setModalPresentationStyle_(2) #2 for sheet, 0 for full screen
	tabVC.presentViewController_animated_completion_(navController, True, None)


if __name__ == '__main__':
	main()
