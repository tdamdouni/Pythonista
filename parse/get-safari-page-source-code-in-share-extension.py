# coding: utf-8

# https://forum.omz-software.com/topic/3117/get-safari-page-source-code-in-share-extension/18

from objc_util import *
storage=ObjCClass('NSHTTPCookieStorage').sharedHTTPCookieStorage()
print(storage.cookies())

# --------------------

cookieData= ObjCClass('NSKeyedArchiver').archivedDataWithRootObject_(storage.cookies())

# --------------------

cookiefile=re.findall(r'/private[^,]*',str(ObjCInstance(storage._cookieStorage()).description()))[0]
cookiedata=open(cookiefile).read()

# --------------------

