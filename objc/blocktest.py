# coding: utf-8

# https://github.com/jsbain/objc_hacks/blob/master/blocktest.py

'''
experiment with blocks.

[theArray enumerateObjectsUsingBlock:^(id obj, NSUInteger idx, BOOL *stop){
    NSLog(@"The object at index %d is %@",idx,obj);
}];
'''
from __future__ import print_function
from ctypes import *
from objc_util import *
import pdb

NSBlock=ObjCClass('NSBlock')
from ctypes import *

ENUMCALLBACK=CFUNCTYPE(None, c_void_p,c_void_p, c_uint, POINTER(c_bool))


class GenericBlockDescriptor(Structure):
   _fields_=[('reserved',c_ulong),
            ('size',c_ulong),
            ('signature', c_char_p)]
   def __init__(self,block):
      self.size=sizeof(block)

class EnumerationBlock(Structure):
   '''
   struct Block_literal_1 {
    void *isa; // initialized to &_NSConcreteStackBlock or &_NSConcreteGlobalBlock
    int flags;
    int reserved;
    void (*invoke)(void *, ...);
    struct Block_descriptor_1 {
    unsigned long int reserved;         // NULL
        unsigned long int size;         // sizeof(struct Block_literal_1)
        // optional helper functions
        void (*copy_helper)(void *dst, void *src);     // IFF (1<<25)
        void (*dispose_helper)(void *src);             // IFF (1<<25)
        // required ABI.2010.3.16
        const char *signature;                         // IFF (1<<30)
    } *descriptor;
    // imported variables
   };'''
   _fields_=  [('isa',c_void_p),
               ('flags',c_int32),
               ('reserved',c_int32),
               ('invoke',ENUMCALLBACK),
               ('descriptor',POINTER(GenericBlockDescriptor))]
   def __init__(self,invoke):        
      self._descriptor=GenericBlockDescriptor(self)
      self.descriptor=pointer(self._descriptor)
      self.isa=NSBlock.ptr
      self.invoke=ENUMCALLBACK(invoke)
      self.descriptor[0].signature=c_char_p('') # not used
      self.descriptor[0].size=sizeof(self)


def invoke_py(self, obj, ind, stop):
   print('The item at index',ind,'is', ObjCInstance(obj))
   if ObjCInstance(obj).intValue()==-1:
      print('stopping here')
      stop[0]=True
      
blk=EnumerationBlock(invoke_py)
A=ns([4,3,7,9,-1, 5])
A.enumerateObjectsUsingBlock_(byref(blk))