# coding: utf-8

# https://gist.github.com/steventroughtonsmith/5f9f2c05c5e3dc6b31d8

from UIKit import *
from Foundation import *
from ctypes import *

libobjc = CDLL('/usr/lib/libobjc.dylib')

QLPreviewController = ObjCClass('QLPreviewController')

@on_main_thread
def main():
	rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
	tabVC = rootVC.detailViewController()
	
	methods = [numberOfSectionsInTableView_, tableView_numberOfRowsInSection_, tableView_cellForRowAtIndexPath_, refresh, tableView_didSelectRowAtIndexPath_, getPath, setPath_, previewController_shouldOpenURL_forPreviewItem_, numberOfPreviewItemsInPreviewController_, previewController_previewItemAtIndex_, setFiles_, getFiles]
	protocols = ['OMTabContent']
	FBFilesTableViewController = create_objc_class('FBFilesTableViewController', UITableViewController, methods=methods, protocols=protocols)
	
	vc = FBFilesTableViewController.alloc().initWithStyle_(0).autorelease()
	vc.setPath_('/')
	vc.refresh()
	vc.title = 'File Browser'
	
	rootNavigationController = UINavigationController.alloc().initWithRootViewController_(vc).autorelease()
	tabVC.addTabWithViewController_(rootNavigationController)
	
def setPath_(_self, _cmd, _path):
	libobjc.objc_setAssociatedObject.argtypes = [c_void_p] * 3 + [c_ulong]
	libobjc.objc_setAssociatedObject(_self, sel('_internalPath'), _path, 3)
	ObjCInstance(_self).title = ObjCInstance(_path).lastPathComponent()
	
def getPath(_self, _cmd):
	libobjc.objc_getAssociatedObject.argtypes = [c_void_p] * 2
	libobjc.objc_getAssociatedObject.restype = c_void_p
	_p = libobjc.objc_getAssociatedObject(_self, sel('_internalPath'))
	return ObjCInstance(_p).ptr
getPath.encoding = '@0@0'

def setFiles_(_self, _cmd, _files):
	libobjc.objc_setAssociatedObject.argtypes = [c_void_p] * 3 + [c_ulong]
	libobjc.objc_setAssociatedObject(_self, sel('_internalFiles'), _files, 1)
	
def getFiles(_self, _cmd):
	libobjc.objc_getAssociatedObject.argtypes = [c_void_p] * 2
	libobjc.objc_getAssociatedObject.restype = c_void_p
	_p = libobjc.objc_getAssociatedObject(_self, sel('_internalFiles'))
	return ObjCInstance(_p).ptr
getFiles.encoding = '@0@0'

def refresh(_self, _cmd):
	path = ObjCInstance(_self).getPath()
	tempFiles = NSFileManager.defaultManager().contentsOfDirectoryAtPath_error_(path, None)
	
	if tempFiles == None or tempFiles.count() == 0:
		if path.isEqualToString_('/System'):
			tempFiles = ns(['Library'])
		elif path.isEqualToString_('/usr'):
			tempFiles = ns(['lib'])
		else:
			tempFiles = NSArray.array()
	ObjCInstance(_self).setFiles_(tempFiles.copy())
	
def numberOfSectionsInTableView_(_self, _cmd, _tv):
	return 1
	
def tableView_numberOfRowsInSection_(_self, _cmd, _tv, _section):
	return ObjCInstance(_self).getFiles().count()
	
def tableView_cellForRowAtIndexPath_(_self, _cmd, _tv, _indexPath):
	identifier = 'FileCell'
	cell = ObjCInstance(_tv).dequeueReusableCellWithIdentifier_(identifier)
	
	if cell == None:
		cell = UITableViewCell.alloc().initWithStyle_reuseIdentifier_(3, identifier)
		
	filename = ObjCInstance(_self).getFiles()[ObjCInstance(_indexPath).row()]
	oldPath = ObjCInstance(_self).getPath()
	newPath = oldPath.stringByAppendingPathComponent_(filename)
	
	cell.textLabel().text = filename
	cell.imageView().image = None
	
	isDir = c_bool()
	fileExists = NSFileManager.defaultManager().fileExistsAtPath_isDirectory_(newPath,byref(isDir))
	
	if isDir:
		cell.imageView().image = UIImage.imageNamed_('Folder')
		
	if filename.hasSuffix_('.png') or filename.hasSuffix_('.jpg'):
		cell.imageView().image = UIImage.imageNamed_('FileImage')
		
	return cell.ptr
	
def tableView_didSelectRowAtIndexPath_(_self, _cmd, _tv, _indexPath):
	FBFilesTableViewController = ObjCClass('FBFilesTableViewController')
	filename = ObjCInstance(_self).getFiles()[ObjCInstance(_indexPath).row()]
	
	oldPath = ObjCInstance(_self).getPath()
	newPath = oldPath.stringByAppendingPathComponent_(filename)
	
	isDir = c_bool()
	NSFileManager.defaultManager().fileExistsAtPath_isDirectory_(newPath,byref(isDir))
	
	if isDir:
		vc = FBFilesTableViewController.alloc().initWithStyle_(0).autorelease()
		vc.setPath_(newPath)
		vc.refresh()
		
		ObjCInstance(_self).showViewController_sender_(vc,ObjCInstance(_self))
	else:
		vc = QLPreviewController.alloc().init().autorelease()
		vc.dataSource = ObjCInstance(_self)
		
		ObjCInstance(_self).showViewController_sender_(vc,ObjCInstance(_self))
		
	ObjCInstance(_tv).deselectRowAtIndexPath_animated_(ObjCInstance(_indexPath), False)
	
def previewController_shouldOpenURL_forPreviewItem_(_self, _cmd, _previewController, _url, _item):
	return True
previewController_shouldOpenURL_forPreviewItem_.encoding = 'B0@0@0:@0@0'

def numberOfPreviewItemsInPreviewController_(_self, _cmd, _previewController):
	return 1
numberOfPreviewItemsInPreviewController_.encoding = 'q0@00@0@0'

def previewController_previewItemAtIndex_(_self, _cmd, _previewController, _index):
	filename = ObjCInstance(_self).getFiles()[ObjCInstance(_self).tableView().indexPathForSelectedRow().row()]
	oldPath = ObjCInstance(_self).getPath()
	newPath = oldPath.stringByAppendingPathComponent_(filename)
	return NSURL.fileURLWithPath_(newPath).ptr
previewController_previewItemAtIndex_.encoding = '@0@0:@0@0'

if __name__ == '__main__':
	main()

