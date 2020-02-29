from __future__ import print_function
# https://forum.omz-software.com/topic/3708/use-objc_util-and-nsurlconnection-to-make-a-get-request/2

from objc_util import *

class Web(object):
	def __init__(self, root=None, method=None, headers=None):
		#NSMutableURLRequest* request = [[NSMutableURLRequest alloc] initWithURL:[NSURL URLWithString:url]];
		self.request = ObjCClass('NSMutableURLRequest').alloc().initWithURL_(nsurl(root))
		#[request setHTTPMethod:@"POST"];
		self.request.setHTTPMethod_(method)
		
		# Make headers
		for key in headers:
			#[request setValue:@"es" forHTTPHeaderField:@"Accept-Language"];
			self.request.setValue_forHTTPHeaderField_(key, headers[key])
			
		# Make request
		#NSURLConnection * theConnection = [[NSURLConnection alloc] initWithRequest:imageRequest delegate:self];
		#self.conn = ObjCClass('NSURLConnection').alloc().initWithRequest_delegate_(self.request, self)
		self.conn = ObjCClass('NSURLConnection').alloc().initWithRequest_delegate_startImmediately_(self.request, self, True)
		
		#[connection autorelease];
		self.conn.autorelease()

import requests

root='http://validate.jsontest.com'
url=root+''
params = {'json':str({"key":"value"})}
r = requests.get(url, params=params)
print(r.json())
