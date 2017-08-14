#!python3

# https://forum.omz-software.com/topic/4212/objc-generics-support

import ui
from objc_util import *

#
# UITableViewDelegate
#

def handler(_cmd, action, index_path):
	print('Trash it tapped')
	
	
def tableView_editActionsForRowAtIndexPath_(self, cmd, table_view, index_path):
	yellow = ObjCClass('UIColor').yellowColor()
	
	block_handler = ObjCBlock(handler, restype=None, argtypes=[c_void_p, c_void_p, c_void_p])
	
	action = ObjCClass('UITableViewRowAction').rowActionWithStyle_title_handler_(0, ns('Trash it!'), block_handler)
	action.setBackgroundColor(yellow)
	
#   return ns([])  <- crash
# return ns([action]) <- crash
	#return None # ok
	return ns([action]).ptr
	
	
def make_table_view_delegate():
	methods = [tableView_editActionsForRowAtIndexPath_]
	protocols = ['UITableViewDelegate']
	delegate = create_objc_class('CustomTableViewDelegate', methods=methods, protocols=protocols)
	return delegate.alloc().init()
	
#
# UITableView
#

table_view = ui.TableView(name='Custom Action', frame=(0, 0, 300, 480))
table_view.data_source = ui.ListDataSource(['Hallo', 'Hi', 'Ciao'])

table_view_objc = ObjCInstance(table_view)
table_view_objc.setDelegate(make_table_view_delegate())

table_view.present('sheet')

