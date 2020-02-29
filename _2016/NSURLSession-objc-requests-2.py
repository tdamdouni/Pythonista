from __future__ import print_function
# https://forum.omz-software.com/topic/3708/use-objc_util-and-nsurlconnection-to-make-a-get-request/4

import objc_util
from urlparse import urlparse
from urllib import urlencode
from ctypes import c_void_p
import time

class Web(object):
	def __init__(self, url=None, params=None):
		self.data = None
		
		if params:
			params_encoded = urlencode(params)
		else:
			params_encoded = ""
		url = objc_util.nsurl("{}?{}".format(url, params_encoded))
		request = objc_util.ObjCClass("NSURLRequest").request(URL=url)
		configuration = objc_util.ObjCClass("NSURLSessionConfiguration").defaultSessionConfiguration()
		
		session = objc_util.ObjCClass("NSURLSession").session(Configuration=configuration)
		
		completionHandler = objc_util.ObjCBlock(self.responseHandlerBlock, restype=None, argtypes=[c_void_p, c_void_p, c_void_p, c_void_p])
		objc_util.retain_global(completionHandler)
		
		dataTask = session.dataTask(Request=request, completionHandler=completionHandler)
		dataTask.resume()
		
	def responseHandlerBlock(self, _cmd, data, response, error):
		if error is not None:
			error = objc_util.ObjCInstance(error)
			print(error)
			return
		response = objc_util.ObjCInstance(response)
		data = objc_util.ObjCInstance(data)
		self.data = (str(objc_util.nsdata_to_bytes(data)))
		
	def return_data(self):
		return self.data
		
		
url = "http://validate.jsontest.com"
params = {"json" : {"first" : "lukas", "last" : "kollmer"}}

#validate(url, None, responseHandlerBlock)
#validate(url, params, responseHandlerBlock)
call = Web(url, params)

wait = True
while wait:
	data = call.return_data()
	if data != None:
		print(data)
		wait = False
print("Done")

