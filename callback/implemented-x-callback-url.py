# https://forum.omz-software.com/topic/3011/share-code-implemented-x-callback-url/5

import x_callback_url

url = 'drafts4://x-callback-url/get?uuid=YOUR_UUID&x-success=pythonista://'
def handler(url_info):
	print(info)
	# Do something with the data passed back to Pythonista (available through url_info.parameters)
	
x_callback_url.open_url(url, handler)

# --------------------

# coding: utf-8

import x_callback_url

url = "working-copy://x-callback-url/status/?repo=MY_REPO&unchanged=1&key=MY_KEY&x-success=pythonista://"

def handler(response):
	print(response)
	
x_callback_url.open_url(url, handler)
# --------------------
# coding: utf-8
import x_callback_url
from objc_util import ObjCInstance

_handler = None
_requestID = None

url = "working-copy://x-callback-url/status/?repo=MY_REPO&unchanged=1&key=MY_KEY&x-success=pythonista://"

def handler(response):
	print(response)
	
x_callback_url.open_url(url, handler)
# --------------------

