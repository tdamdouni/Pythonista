# https://forum.omz-software.com/topic/3800/touch-id

# Try using

# c_void_p(error.ptr)

# rather than

# c_void_p(id(error))

# -- you were pointing to the python object using id, not the objc object!

from objc_util import  *
from ctypes import *
import dialogs

def block(_cmd, succeed, error_ptr):
    pass

context = ObjCClass('LAContext').alloc().init()
error = ObjCClass('NSError').alloc().init()
print(context.canEvaluatePolicy_error_(1, c_void_p(id(error))))
context.evaluatePolicy_localizedReason_reply_(1, 'Touch ID', ObjCBlock(block, restype = None, argtypes = [c_void_p, c_bool, c_void_p]))
