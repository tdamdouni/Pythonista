import ui
from ctypes import py_object
from objc_util import *
import sys
from objc_classes import objcmethod,  objcclass

UISearchController=ObjCClass('UISearchController')

class SearchableTableView(ui.View):
	'''Works like a tableview, except that search bar is shown.  
	TODO: Extra search_delegate attrib, exposes:
		update_search_results(tv, searchbar)
		scope_button_titles(tv)
	'''
	def __init__(self,*args,**kwargs):
		#setup a tableview
		ui.View.__init__(self,*args,**kwargs)
		tv=ui.TableView(name='tv1',*args,**kwargs)
		self.bounds=tv.frame
		tv.flex='wh'
		self.add_subview(tv)
		searchController=UISearchController.alloc().initWithSearchResultsController_(None)
		updater = MySearchResultUpdater()
		searchController.searchResultsUpdater = updater
		self.updater=updater
		updater.tv=self
		searchController.dimsBackgroundDuringPresentation = False #True prevents selection
		searchController.definesPresentationContext = False
		searchController.hidesNavigationBarDuringPresentation=False #don't change this'
		#searchController.searchBar().scopeButtonTitles=ns(['A','B']) # this doesnt work..
		#searchController.searchBar().sizeToFit()
		self.tv=tv
		self.searchController = searchController
		ObjCInstance(self.tv).tableHeaderView = searchController.searchBar()
	def __getattribute__(self,attr):
		'''Mock most attributes to tableview, except for the ones listed'''
		attrlist=['left_button_items', 'y', 'flex', 'touch_enabled', 'superview', 'x', 'transform', 'navigation_view', 'present', 'on_screen', 'close', 'bring_to_front', 'frame', 'center', 'width', 'send_to_back', 'add_subview', 'name', 'autoresizing', 'subviews', 'bounds', 'wait_modal', 'remove_subview', 'right_button_items','tv']

		if not (attr.startswith('_') or attr in attrlist) and hasattr(self.tv,attr):
				return getattr(self.tv, attr)
		else:
			return object.__getattribute__(self,attr)
	def __setattr__(self,attr,value):
		attrlist=['left_button_items', 'y', 'flex', 'touch_enabled', 'superview', 'x', 'transform', 'navigation_view', 'present', 'on_screen', 'close', 'bring_to_front', 'frame', 'center', 'width', 'send_to_back', 'add_subview', 'name', 'autoresizing', 'subviews', 'bounds', 'wait_modal', 'remove_subview', 'right_button_items','tv']

		if not (attr.startswith('_') or attr in attrlist) and hasattr(self,'tv') and hasattr(self.tv,attr):
			setattr(self.tv, attr,value)
		else:
			object.__setattr__(self,attr,value)
			
@objcclass
class MySearchResultUpdater(object):
	'''TODO: implement this as a standard delegate, and have a python search_delegate'''
	protocol=['UISearchControllerUpdating']
	def __init_(self):
		self.tv=None
	
	@objcmethod
	def updateSearchResultsForSearchController_(_self,_sel, controller):			
		tv=MySearchResultUpdater(_self).tv
		if ObjCInstance(controller).active():
			sb=ObjCInstance(controller).searchBar()
			filterTerm=str(sb.text())
			tv.data_source.filter_items(filterTerm)
		else:
			tv.data_source.filter_items('')
			
class FilteredListDataSource(ui.ListDataSource):
	'''TOdo: deleting and moving items does not work. '''
	def __init__(self, items=None, filter=''):
		ui.ListDataSource.__init__(self,items)
		self._allitems=list(self._items)
	def filter_items(self,filt):
		if not filt:
			self._items=list(self._allitems)
		else:
			self._items=[item for item in list(self._allitems) if filt in item]
		self.reload()

	@property
	def items(self):
		return self._items
	
	@items.setter
	def items(self, value):
		self._allitems = ui.ListDataSourceList(value, self)
		self._items=self._allitems
		self.reload() 

	
if __name__=='__main__':
	L=FilteredListDataSource(['hello','world','this','is','a','test'])
	stv=SearchableTableView(frame=(0,0,200,700))
	stv.data_source=stv.delegate=L
	stv.present('panel')



