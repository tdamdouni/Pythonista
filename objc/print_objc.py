# coding: utf-8

# https://github.com/jsbain/objc_hacks/blob/master/print_objc.py

from __future__ import print_function
from objc_util import *
import ctypes

def parse_encoding(enc):
   type_names={'c':'char',
   'i':'int',
   's':'short',
   'l':'long',
   'q':'long long',
   'C':'unsigned char',
   'I':'unsigned int',
   'S':'unsigned short',
   'Q':'unsigned long long',
   'f':'float',    
   'd':'double',
   'B':'bool',
   'v':'void',
   '*':'char *',
   '@':'object',
   '#':'class',
   ':':'method',
   '^':'pointer',
   '?':'unknown'}

   def parse(c):
      return c.startswith('^')*'*' + type_names.get(c.split('^')[-1],c.split('^')[-1])
   enc=re.split(r'\d*',enc)
   signature = [parse(c) for c in enc if c]

   return signature
  #missing bnum. bit field, []array, {}struct, ()union


   #objc_property_t * class_copyPropertyList ( Class cls, unsigned int *outCount );
   


    
def get_methods(objc_class):
    '''return list of selector name, and string ret type and arg types'''
    free = c.free
    free.argtypes = [c_void_p]
    free.restype = None
    class_copyMethodList = c.class_copyMethodList
    class_copyMethodList.restype = ctypes.POINTER(c_void_p)
    class_copyMethodList.argtypes = [c_void_p, ctypes.POINTER(ctypes.c_uint)]
    

    method_getName = c.method_getName
    method_getName.restype = c_void_p
    method_getName.argtypes = [c_void_p]
    
    method_getTypeEncoding=c.method_getTypeEncoding;
    method_getTypeEncoding.restype =c_char_p
    method_getTypeEncoding.argtypes= [ c_void_p ]
    


    #DumpObjcMethods(object_getClass(yourClass) /* Metaclass */);
    py_methods = []
    num_methods = c_uint(0)
    method_list_ptr = class_copyMethodList(objc_class.ptr, ctypes.byref(num_methods))
    for i in xrange(num_methods.value):
        selector = method_getName(method_list_ptr[i])
        enc=method_getTypeEncoding(method_list_ptr[i])
        penc=parse_encoding(enc)
        sel_name = sel_getName(selector)
        py_method_name = sel_name.replace(':', '_')
        
        #py_methods.append(enc[0]+' ' +py_method_name+'('+', '.join(enc[3:])+')')
        py_methods.append((py_method_name, penc[0],penc[3:]))
    free(method_list_ptr)
    return sorted(py_methods)
    
def get_class_methods(objc_class):
    '''get class methods'''
    object_getClass = c.object_getClass
    object_getClass.restype = c_void_p
    object_getClass.argtypes = [c_void_p]
    meta=ObjCInstance(object_getClass(objc_class))
    return get_methods(meta)

import console
def print_methods(clsname,print_private=False):
   cls=ObjCClass(clsname)
   console.set_color(1,0,0)
   print(clsname)
   print('Class Methods______')
   console.set_color(0,0,0)
   m=get_class_methods(cls)
   print('\n'.join([(k[1]+' ' +k[0]+'( '+', '.join(k[2])+' )') for k in m if not k[0].startswith('_')]))
   if print_private:
         print('\n'.join([(k[1]+' ' +k[0]+'( '+', '.join(k[2])+' )') for k in m if k[0].startswith('_')]))
   console.set_color(1,0,0)
   print('_______Instance Methods______')
   console.set_color(0,0,0)
   m=get_methods(cls)
   print('\n'.join([(k[1]+'\t' +k[0]+'( '+', '.join(k[2])+' )') for k in m if not k[0].startswith('_')]))
   if print_private:
         print('\n'.join([(k[1]+'\t' +k[0]+'( '+', '.join(k[2])+' )') for k in m if k[0].startswith('_')]))