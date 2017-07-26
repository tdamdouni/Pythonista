#!/usr/bin/env python3

# https://forum.omz-software.com/topic/3708/use-objc_util-and-nsurlconnection-to-make-a-get-request/3

import objc_util
import urllib.parse
from ctypes import c_void_p

NSURLRequest = objc_util.ObjCClass("NSURLRequest")
NSURLSession = objc_util.ObjCClass("NSURLSession")
NSURLSessionConfiguration = objc_util.ObjCClass("NSURLSessionConfiguration")


def validate(url, params, responseHandler):
	if params:
		params_encoded = urllib.parse.urlencode(params)
	else:
		params_encoded = ""
	url = objc_util.nsurl("{}?{}".format(url, params_encoded))
	request = NSURLRequest.request(URL=url)
	configuration = NSURLSessionConfiguration.defaultSessionConfiguration()
	
	session = NSURLSession.session(Configuration=configuration)
	
	completionHandler = objc_util.ObjCBlock(responseHandler, restype=None, argtypes=[c_void_p, c_void_p, c_void_p, c_void_p])
	objc_util.retain_global(completionHandler)
	
	dataTask = session.dataTask(Request=request, completionHandler=completionHandler)
	dataTask.resume()
	
def responseHandlerBlock(_cmd, data, response, error):
	if error is not None:
		error = objc_util.ObjCInstance(error)
		print(error)
		return
	response = objc_util.ObjCInstance(response)
	data = objc_util.ObjCInstance(data)
	print(str(objc_util.nsdata_to_bytes(data)))
	
url = "http://validate.jsontest.com"
params = {"json" : {"first" : "lukas", "last" : "kollmer"}}

validate(url, None, responseHandlerBlock)

