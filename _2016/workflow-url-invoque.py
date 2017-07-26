# https://forum.omz-software.com/topic/3920/pythonista-to-call-workflow-and-return/2

try:
	from urllib.parse import quote_plus, urlencode  # Python 3
except ImportError:
	from urllib import quote_plus, urlencode        # Python 2
import requests


def url_finish(*args, **kwargs):
	"""completes the right side of a url.
	URLs for REST APIs are composed of three parts:
	1. Base URL: workflow://x-callback-url
	2. Path Parameters (args) separated by /'s
	3. Query Parameters (kwargs) started with a ? and then urlencoded
	args are a tuple of unnamed values that go on the left of the ?
	kwargs are a dict of named values that are urlencoded to right of ?"""
	s = ''
	if args:
		s = '/' + quote_plus('/'.join(str(arg) for arg in args), safe='/')
	if kwargs:
		s += '?' + urlencode(kwargs)
	return s
	
	
base_url = 'workflow://x-callback-url'
url = base_url + url_finish('run-workflow', name='Play Specific', success='pythonista://ferny_launch')
print(url)
requests.get(url)

