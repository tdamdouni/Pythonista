# coding: utf-8

# Captured from: _https://forum.omz-software.com/topic/2520/listing-all-editor-tabs_


# coding: utf-8
from objc_util import *

UIApplication=ObjCClass('UIApplication')
app=UIApplication.sharedApplication()

def saveTabRestorationInfo():
	app.delegate().viewController().saveTabRestorationInfo()
	
def list_editor_open_files():
	return [str(x) for x in app.delegate().viewController().allOpenFilePaths()]

