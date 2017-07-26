# https://forum.omz-software.com/topic/3146/share-code-get-available-memory/3

from objc_util import *

NSProcessInfo = ObjCClass('NSProcessInfo')
processInfo = NSProcessInfo.processInfo()
print(processInfo.activeProcessorCount())
