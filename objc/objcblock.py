# coding: utf-8

# https://github.com/jsbain/objc_hacks/blob/master/objcblock.py

''' block factory
ObjCBlock(py_callback,restype, argtypes[])
'''
from __future__ import print_function

from ctypes import *
from objc_util import *
import pdb
NSBlock=ObjCClass('NSBlock')
class ObjCBlockDescriptor(Structure):
   _fields_=[('reserved',c_ulong),
         ('size',c_ulong),
         ('signature', c_char_p)]
   def __init__(self,block):
      self.size=sizeof(block)
ENUMCALLBACK=CFUNCTYPE(None, c_void_p,c_void_p, c_uint, POINTER(c_bool))
def ObjCBlock(invoke,restype,argtypes):
      BLOCK_FUNC = CFUNCTYPE(restype,c_void_p,*argtypes)
      class Block(Structure):
         _fields_=  [('isa',c_void_p),
               ('flags',c_int32),
               ('reserved',c_int32),
               ('invoke',BLOCK_FUNC),
               ('descriptor',POINTER(ObjCBlockDescriptor))]   
         def __init__(self):
            self._descriptor=ObjCBlockDescriptor(self)
            self.descriptor=pointer(self._descriptor)
            self.isa=NSBlock.ptr
            self.invoke=BLOCK_FUNC(invoke)
            self.descriptor[0].signature=c_char_p('') # not used
            self.descriptor[0].size=sizeof(self)
      return byref(Block())
if __name__=='__main__':
   def invoke_py(self, obj, idx, stop):
      print(self, idx  , obj)
   blk=ObjCBlock(invoke_py,None,[c_void_p,c_uint, POINTER(c_bool)])
      
   A=ns(['a',1,3])
   A.enumerateObjectsUsingBlock_(blk)
#A.enumerate