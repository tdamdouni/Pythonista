# coding: utf-8

# https://gist.github.com/shaun-h/e86a8a3b5ea2ca16f136

from objc_util import *
import ui
from collections import OrderedDict

UITableView = ObjCClass('UITableView')
UITableViewCell = ObjCClass('UITableViewCell')

class UITableViewStyle(object):
	UITableViewStylePlain = 0
	UITableViewStyleGrouped = 1
	
def test_data(number):
	data = OrderedDict()
	valueRange = 10
	for i in range(0,number):
		ii = i * valueRange
		key = str(ii)
		value = []
		for j in range(ii,ii+valueRange):
			value.append(str(j))
		data[key] = value
	return data
	
data = test_data(100)

def tableView_cellForRowAtIndexPath_(self,cmd,tableView,indexPath):
	ip = ObjCInstance(indexPath)
	cell = ObjCInstance(tableView).dequeueReusableCellWithIdentifier_('mycell')
	
	if cell == None:
		cell = UITableViewCell.alloc().initWithStyle_reuseIdentifier_(0,'mycell')
	key = data.keys()[ip.section()]
	text = ns(data[key][ip.row()])
	cell.textLabel().setText_(text)
	
	return cell.ptr
	
def numberOfSectionsInTableView_(self,cmd,tableView):
	return len(data)
	
def tableView_numberOfRowsInSection_(self,cmd, tableView,section):
	key = data.keys()[section]
	return ns(len(data[key])).integerValue()
	
def sectionIndexTitlesForTableView_(self,cmd,tableView):
	return ns(data.keys()).ptr
	
def tableView_sectionForSectionIndexTitle_atIndex_(self,cmd,tableView,title,index):
	#I have assumed order and number of list is the same from list and sections
	return index
	
def tableView_titleForHeaderInSection_(self,cmd,tableView,section):
	return ns('Header for ' + data.keys()[section]).ptr
	
def tableView_titleForFooterInSection_(self,cmd,tableView,section):
	return ns('Footer for ' + data.keys()[section]).ptr
	
#def tableView_commitEditingStyle_forRowAtIndexPath_(self,cmd,tableView,editingStyle,indexPath):
	#pass
	
#def tableView_canEditRowAtIndexPath_(self,cmd,tableView,indexPath):
	#pass
	
#def tableView_canMoveRowAtIndexPath_(self,cmd,tableView,indexPath):
	#pass
	
#def tableView_moveRowAtIndexPath_toIndexPath_(self,cmd,tableView,fromIndexPath,toIndexPath):
	#pass
	
	
	
methods = [tableView_cellForRowAtIndexPath_,tableView_numberOfRowsInSection_,numberOfSectionsInTableView_,tableView_titleForHeaderInSection_,tableView_sectionForSectionIndexTitle_atIndex_,sectionIndexTitlesForTableView_,tableView_titleForFooterInSection_]
protocols = ['UITableViewDataSource']
TVDataSourceAndDelegate = create_objc_class('TVDataSourceAndDelegate', NSObject, methods=methods, protocols=protocols)

class MyTableView(ui.View):
	@on_main_thread
	def __init__(self, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		frame = CGRect(CGPoint(0, 0), CGSize(self.width, self.height))
		self.tableView = UITableView.alloc().initWithFrame_style_(frame, UITableViewStyle.UITableViewStylePlain)
		flex_width, flex_height = (1<<1), (1<<4)
		self.tableView.setAutoresizingMask_(flex_width|flex_height)
		
		#set delegate
		self.tb_ds = TVDataSourceAndDelegate.alloc().init().autorelease()
		self.tableView.setDataSource_(self.tb_ds)
		self_objc = ObjCInstance(self)
		self_objc.addSubview_(self.tableView)
		self.tableView.release()
		
if __name__ == '__main__':
	wv = MyTableView()
	wv.present()

