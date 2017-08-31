# https://forum.omz-software.com/topic/3011/share-code-implemented-x-callback-url

UIApplication -openURL:sourceApplication:annotation:# --------------------
-openURL:# --------------------
-openURL:# --------------------
pythonista://# --------------------
import x_callback_url

url = 'drafts4://x-callback-url/get?uuid=YOUR_UUID&x-success=pythonista://'
def handler(url_info):
    print(info)
    # Do something with the data passed back to Pythonista (available through url_info.parameters)

x_callback_url.open_url(url, handler)
# --------------------
x_callback_url.open_url()# --------------------
x-success# --------------------
x-source# --------------------
x-error# --------------------
x-success# --------------------
# coding: utf-8
import x_callback_url

url = "working-copy://x-callback-url/status/?repo=MY_REPO&unchanged=1&key=MY_KEY&x-success=pythonista://"

def handler(response):
    print(response)

x_callback_url.open_url(url, handler)
# --------------------
Traceback (most recent call last):
  File "_ctypes/callbacks.c", line 314, in 'calling callback function'
  File "/private/var/mobile/Containers/Shared/AppGroup/84B2FC5A-8F6A-4B20-BA21-BE5B5A07629F/Documents/site-packages/x_callback_url.py", line 32, in application_openURL_sourceApplication_annotation_
    url_str = str(ObjCInstance(url))
NameError: global name 'ObjCInstance' is not defined
# --------------------
from objc_utils import ObjCInstance# --------------------
NameError: global name 'c' is not defined
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
from objc_util import *# --------------------
_requestID# --------------------
_handler# --------------------
None# --------------------
_# --------------------
_requestID# --------------------
_handler# --------------------
g_requestID# --------------------
g_handler# --------------------
from objc_utils import *# --------------------
app://xcallbackresponse-REQUEST_ID/?query=value&query=value# --------------------
app://xcallbackresponse-REQUEST_IDvalue# --------------------
x_callback_response.parameters# --------------------
None# --------------------
x_callback_response.raw_response_data# --------------------
app://xcallbackresponse-REQUEST_ID# --------------------
Traceback (most recent call last):
  File "_ctypes/callbacks.c", line 234, in 'calling callback function'
  File "/private/var/mobile/Containers/Shared/AppGroup/74CC34ED-493E-431F-9C45-5BD2EF3B2AE0/Pythonista3/Documents/firebaseapp/swizzle.py", line 146, in saveData
  File "/var/containers/Bundle/Application/71C9338F-1BD7-4D52-9DAD-EE24DDF5139E/Pythonista3.app/Frameworks/Py3Kit.framework/pylib/site-packages/objc_util.py", line 796, in __call__
    method_name, kwarg_order = resolve_instance_method(obj, self.name, args, kwargs)
  File "/var/containers/Bundle/Application/71C9338F-1BD7-4D52-9DAD-EE24DDF5139E/Pythonista3.app/Frameworks/Py3Kit.framework/pylib/site-packages/objc_util.py", line 403, in resolve_instance_method
    raise AttributeError('No method found for %s' % (name,))
AttributeError: No method found for originalsaveData
# --------------------
