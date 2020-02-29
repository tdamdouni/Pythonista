from __future__ import print_function
# https://forum.omz-software.com/topic/2152/help-with-blocks-again
# coding: utf-8
from objc_util import *

UUID = '1234abcd'
TITLE = 'Pythonista Spotlight Test'
TEXT = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla rhoncus rutrum ornare. Integer ac dolor.'

CoreSpotlight = NSBundle.bundleWithPath_('/System/Library/Frameworks/CoreSpotlight.framework')
CoreSpotlight.load()

CSSearchableItem = ObjCClass('CSSearchableItem')
CSSearchableIndex = ObjCClass('CSSearchableIndex')
CSSearchableItemAttributeSet = ObjCClass('CSSearchableItemAttributeSet')

idx = CSSearchableIndex.defaultSearchableIndex()
attr_set = CSSearchableItemAttributeSet.alloc().initWithItemContentType_('public.text')
attr_set.setTitle_(TITLE)
attr_set.setContentDescription_(TEXT)

item = CSSearchableItem.alloc().initWithUniqueIdentifier_domainIdentifier_attributeSet_(UUID, None, attr_set)

def handler_func(_cmd, error):
    print('Completion handler called')
    if error:
        print(ObjCInstance(error))

handler= ObjCBlock(handler_func, restype=None, argtypes=[c_void_p, c_void_p])
idx.indexSearchableItems_completionHandler_([item], handler)

item.release()
attr_set.release()