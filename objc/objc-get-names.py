# coding: utf-8

# https://forum.omz-software.com/topic/2808/bug-objc_util-and-dir

from objc_util import ObjCClass
print('\n'.join(ObjCClass.get_names('OM')))
