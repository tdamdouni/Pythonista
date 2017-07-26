# coding: utf-8
import swizzle
from objc_util import *
import ctypes
import json, urllib
import uuid
import sys
import webbrowser

NSURLComponents = ObjCClass('NSURLComponents')
appDelegate = UIApplication.sharedApplication().delegate()
_handler = None
_requestID = None

class x_callback_response (object):
	full_url = None
	source_app = None
	parameters = None
	
	def __str__(self):
		return '<x_callback_response: source_app = {}, parameters = {}>'.format(self.source_app, self.parameters)

def open_url(url, handler):
	global _handler
	global _requestID
	_requestID = uuid.uuid1()
	_handler = handler
	url_with_uuid = url + 'xcallbackresponse-' + str(_requestID)
	webbrowser.open(url_with_uuid)

def application_openURL_sourceApplication_annotation_(_self, _sel, app, url, source_app, annotation):
	url_str = str(ObjCInstance(url))
	
	if not 'xcallbackresponse-' + str(_requestID) in url_str:
		print('not from x-callback-url, will run original function')
		obj = ObjCInstance(_self)
		original_method = getattr(obj, 'original'+c.sel_getName(_sel), None)
		if original_method:
			_annotation = ObjCInstance(annotation) if annotation else None
			return original_method(ObjCInstance(app), ObjCInstance(url), ObjCInstance(source_app), _annotation)
	else:
		x_callback_info = x_callback_response()
		x_callback_info.full_url = url_str
		x_callback_info.source_app = str(ObjCInstance(source_app))
		
		query = NSURLComponents.componentsWithURL_resolvingAgainstBaseURL_(nsurl(url_str), False)
		x_callback_info.parameters = dict()
		for queryItem in query.queryItems():
			x_callback_info.parameters[str(queryItem.name())] = str(queryItem.value())
			
		if _handler:
			_handler(x_callback_info)
		return True



# Do the swizzling
cls = ObjCInstance(c.object_getClass(appDelegate.ptr))
swizzle.swizzle(cls, 'application:openURL:sourceApplication:annotation:', application_openURL_sourceApplication_annotation_)




if __name__ == '__main__':
	import console
	console.clear()
	
	draft_uuid = '9B0A1EF8-B2D8-4050-8EE4-B6D8AC0F229B'
	url = 'drafts4://x-callback-url/get?uuid={}&x-success=pythonista://'.format(draft_uuid)
	
	def my_handler(info):
		print(info.full_url)
		print(info.parameters['text'])
	
	open_url(url, my_handler)
