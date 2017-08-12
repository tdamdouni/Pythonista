# https://forum.omz-software.com/topic/4239/clearing-webview-cache/2

from objc_util import ObjCClass

NSURLCache = ObjCClass('NSURLCache')
shared_cache = NSURLCache.alloc().initWithMemoryCapacity_diskCapacity_diskPath_(0, 0, None)
NSURLCache.setSharedURLCache_(shared_cache)