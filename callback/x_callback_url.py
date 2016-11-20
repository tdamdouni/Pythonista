# coding: utf-8

# https://github.com/lukaskollmer/pythonista-scripts/blob/master/x-callback-url/x_callback_url.py

# https://forum.omz-software.com/topic/3011/share-code-implemented-x-callback-url

# Pythonista  [Share Code] Implemented x-callback-url 

# This morning I asked if I is possible to use x-callback-urls with Pythonista and access data other apps provide. I did some experimentation and came up with a script that is working perfectly.

# What it does:

# Add support for x-callback.urls to Pythonista
# Replace the default UIApplication -openURL:sourceApplication:annotation: method with a custom one (Using @JonB's swizzle.py)
# The custom -openURL: method checks if the url that is opened is the callback from the other app
# If the url is from the other app, a handler function that you provide will be called, with some information about the url as a parameter

# Passed information includes:
	
# The full url called
# The app that opened the callback-url
# A dictionary containing all parameters and their values from the url (This is where you get data you requested from another app)

# If the url is NOT in response to the x-callback-url, Pythonistas default -openURL_ will be called, with all parameters passed to the swizzled one. This ensures that other scripts using the pythonista::// url scheme to open/launch files still work.

#How to use it:
	
# (Using Drafts as an example, works with any app that supports x-callback-urls)

# import x_callback_url

# url = 'drafts4://x-callback-url/get?uuid=YOUR_UUID&x-success=pythonista://'
# def handler(url_info):
#     print(info)
    # Do something with the data passed back to Pythonista (available through url_info.parameters)

# x_callback_url.open_url(url, handler)

# If you don't want to do anything with data passed back to Pythonista, you can omit the handler parameter and just pass the url to x_callback_url.open_url() function
# This currently supports only the x-success parameter, I'll add support for x-source and x-error at a later point (x-success is by far the most important one)


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
		original_method = getattr(obj,'original'+c.sel_getName(_sel),None)
		if original_method:
			if annotation:
				_annotation = ObjCInstance(annotation)
			else:
				_annotation = None
			return original_method(ObjCInstance(app), ObjCInstance(url), ObjCInstance(source_app), _annotation)
	else:
		x_callback_info = x_callback_response()
		x_callback_info.full_url = url_str
		x_callback_info.source_app = str(ObjCInstance(source_app))
		
		query = NSURLComponents.componentsWithURL_resolvingAgainstBaseURL_(nsurl(url_str), False)
		x_callback_info.parameters = dict()
		for queryItem in query.queryItems():
			x_callback_info.parameters[str(queryItem.name())] = str(queryItem.value())
			
		if not _handler == None:
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
