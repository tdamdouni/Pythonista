# coding: utf-8

# https://forum.omz-software.com/topic/2889/getting-pyobject-from-objc-object

# okay, cast is the answer... given an ObjCInstance of a view that started in python...

o.pyObject.encoding='^80:4'
ctypes.cast(o.pyObject(),ctypes.py_object).value

