from __future__ import print_function
# https://gist.github.com/omz/9b918c98d3f6bd66c1cc

# Print system proxy settings using CFNetwork
# NOTE: Requires Pythonista 1.6 (currently in beta)

from objc_util import *

CFNetworkCopySystemProxySettings = c.CFNetworkCopySystemProxySettings
CFNetworkCopySystemProxySettings.restype = c_void_p
CFNetworkCopySystemProxySettings.argtypes = []

proxy_settings = ObjCInstance(CFNetworkCopySystemProxySettings())

print(proxy_settings)