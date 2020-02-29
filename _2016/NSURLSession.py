#!python2

# https://gist.github.com/tlinnet/31b35136e206ea2b4829a13799c89316

from __future__ import print_function
from urlparse import urlparse
from urllib import urlencode
from ctypes import c_void_p
import json
import base64


# pythonista
import objc_util

class Requests(object):
	def __init__(self):
		self.data = None
		
	def get(self, url=None, auth=None, headers=None, params=None):
		# Make url
		if params:
			params_encoded = urlencode(params)
		else:
			params_encoded = ""
			
		url = objc_util.nsurl("{}?{}".format(url, params_encoded))
		
		#request = objc_util.ObjCClass("NSURLRequest").request(URL=url)
		request = objc_util.ObjCClass('NSMutableURLRequest').alloc().initWithURL_(url)
		
		# Make headers
		if headers:
			for key in headers:
				request.setValue_forHTTPHeaderField_(headers[key], key)
				
		if auth:
			userName, password  = auth
			authStr = "%s:%s"%(userName, password)
			authencode = base64.b64encode(bytes(authStr))
			request.addValue_forHTTPHeaderField_("Basic %s"%authencode, "Authorization")
			
		configuration = objc_util.ObjCClass("NSURLSessionConfiguration").defaultSessionConfiguration()
		session = objc_util.ObjCClass("NSURLSession").session(Configuration=configuration)
		
		completionHandler = objc_util.ObjCBlock(self.responseHandlerBlock, restype=None, argtypes=[c_void_p, c_void_p, c_void_p, c_void_p])
		objc_util.retain_global(completionHandler)
		
		dataTask = session.dataTask(Request=request, completionHandler=completionHandler)
		dataTask.resume()
		
		# Wait for completions
		wait = True
		while wait:
			if self.data != None:
				wait = False
		return json.loads(self.data)
		
	def responseHandlerBlock(self, _cmd, data, response, error):
		if error is not None:
			error = objc_util.ObjCInstance(error)
			print(error)
			return
		response = objc_util.ObjCInstance(response)
		data = objc_util.ObjCInstance(data)
		self.data = objc_util.nsdata_to_bytes(data)
		
		
#url = "http://validate.jsontest.com"
#params = {"json" : {"first" : "lukas", "last" : "kollmer"}}
#headers = None
#auth = None

APIKEY = 'SECRET'
#url = 'https://api.hotspotsystem.com/v2.0'+'/locations/'+'4'+'/vouchers'
#params = {"limit" : "4"}
#headers = {'sn-apikey': APIKEY}
#auth = None

url = 'https://api.hotspotsystem.com/v1.0'+'/locations/'+'4'+'/vouchers.json'
params = {"limit" : "4"}
headers = None
auth = (APIKEY, "x")

data = Requests().get(url=url, auth=auth, headers=headers, params=params)
print(data)
print(type(data))
print("Done")

