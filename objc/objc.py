# text encoding: utf-8

# https://github.com/jsbain/objc_hacks/blob/master/objc.py

#. copy of objc_utils with fixed 32 bit stret, and __dir__ functionality

try:
   import ctypes
except ImportError:
   raise NotImplementedError("objc_util requires ctypes, which doesn't seem to be available.")

from ctypes import Structure, sizeof, cdll, c_void_p, c_char, c_char_p, c_double, c_float, c_int, c_longlong, c_short, c_bool, c_long, c_int32, c_ubyte, c_uint, c_ushort, c_ulong, c_ulonglong
import re
import sys
import os
import itertools
import weakref

c = cdll.LoadLibrary(None)

class_getName = c.class_getName
class_getName.restype = c_char_p
class_getName.argtypes = [c_void_p]

class_getSuperclass = c.class_getSuperclass
class_getSuperclass.restype = c_void_p
class_getSuperclass.argtypes = [c_void_p]

class_addMethod = c.class_addMethod
class_addMethod.restype = c_bool
class_addMethod.argtypes = [c_void_p, c_void_p, c_void_p, c_char_p]

class_getInstanceMethod = c.class_getInstanceMethod
class_getInstanceMethod.restype = c_void_p
class_getInstanceMethod.argtypes = [c_void_p, c_void_p]

class_getClassMethod = c.class_getClassMethod
class_getClassMethod.restype = c_void_p
class_getClassMethod.argtypes = [c_void_p, c_void_p]

objc_allocateClassPair = c.objc_allocateClassPair
objc_allocateClassPair.restype = c_void_p
objc_allocateClassPair.argtypes = [c_void_p, c_char_p, c_int]

objc_registerClassPair = c.objc_registerClassPair
objc_registerClassPair.restype = None
objc_registerClassPair.argtypes = [c_void_p]

objc_getClass = c.objc_getClass
objc_getClass.argtypes = [c_char_p]
objc_getClass.restype = c_void_p

method_getTypeEncoding = c.method_getTypeEncoding
method_getTypeEncoding.argtypes = [c_void_p]
method_getTypeEncoding.restype = c_char_p

sel_getName = c.sel_getName
sel_getName.restype = c_char_p
sel_getName.argtypes = [c_void_p]

sel_registerName = c.sel_registerName
sel_registerName.restype = c_void_p
sel_registerName.argtypes = [c_char_p]

object_getClass = c.object_getClass
object_getClass.argtypes = [c_void_p]
object_getClass.restype = c_void_p


LP64 = (sizeof(c_void_p) == 8)
CGFloat = c_double if LP64 else c_float
NSInteger = c_long if LP64 else c_int
NSUInteger = c_ulong if LP64 else c_uint

NSNotFound = sys.maxint

NSUTF8StringEncoding = 4
NS_UTF8 = NSUTF8StringEncoding

class CGPoint (Structure):
   _fields_ = [('x', CGFloat), ('y', CGFloat)]

class CGSize (Structure):
   _fields_ = [('width', CGFloat), ('height', CGFloat)]

class CGVector (Structure):
   _fields_ = [('dx', CGFloat), ('dy', CGFloat)]

class CGRect (Structure):
   _fields_ = [('origin', CGPoint), ('size', CGSize)]
   def __repr__(self):
      return (self.origin.x, self.origin.y, self.size.width, self.size.height).__repr__()

class CGAffineTransform (Structure):
   _fields_ = [('a', CGFloat), ('b', CGFloat), ('c', CGFloat), ('d', CGFloat), ('tx', CGFloat), ('ty', CGFloat)]

class UIEdgeInsets (Structure):
   _fields_ = [('top', CGFloat), ('left', CGFloat), ('bottom', CGFloat), ('right', CGFloat)]

class NSRange (Structure):
   _fields_ = [('location', NSUInteger), ('length', NSUInteger)]

# c.f. https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtTypeEncodings.html
type_encodings = {'c': c_char, 'i': c_int, 's': c_short, 'l': c_int32, 'q': c_longlong,
                  'C': c_ubyte, 'I': c_uint, 'S': c_ushort, 'L': c_ulong, 'Q': c_ulonglong,
                  'f': c_float, 'd': c_double, 'B': c_bool, 'v': None, '*': c_char_p,
                  '@': c_void_p, '#': c_void_p, ':': c_void_p,
                  '{CGPoint}': CGPoint, '{CGSize}': CGSize, '{CGRect}': CGRect, '{CGVector}': CGVector,
                  '{CGAffineTransform}': CGAffineTransform, '{UIEdgeInsets}': UIEdgeInsets, '{_NSRange}': NSRange,
                  '?': c_void_p, '@?': c_void_p
}

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



def get_methods(objc_class):
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
   object_getClass = c.object_getClass
   object_getClass.restype = c_void_p
   object_getClass.argtypes = [c_void_p]
   meta=ObjCInstance(object_getClass(objc_class))
   return get_methods(meta)






def parse_types(type_encoding):
   '''Take an Objective-C type encoding string and convert it to a tuple of (restype, argtypes) appropriate for objc_msgSend()'''
   # NOTE: Structs are only supported for very common (known) cases (CGRect, CGPoint...). Unions and function pointers (blocks) are not supported at all.
   def get_type_for_code(enc_str):
      if enc_str[0] in 'rnNoORV': #const, in, inout... don't care about these
         enc_str = enc_str[1:]
      if enc_str[0] in '^[': #pointer or array
         return c_void_p
      if enc_str.startswith('{'):
         struct_name = enc_str[0:enc_str.find('=')] + '}'
         enc_str = struct_name
      try:
         t = type_encodings[enc_str]
         return t
      except KeyError:
         raise NotImplementedError('Unsupported type encoding (%s)' % (enc_str,))
   encoded_types = filter(lambda x: bool(x), re.split(r'\d', type_encoding))
   encoded_argtypes = encoded_types[3:]
   argtypes = [get_type_for_code(x) for x in encoded_argtypes]
   restype = get_type_for_code(encoded_types[0])
   return (restype, [c_void_p, c_void_p] + argtypes)

def sel(sel_name):
   '''Convenience function to convert a string to a selector'''
   return c.sel_registerName(sel_name)

class ObjCClass (object):
   '''Wrapper for a pointer to an Objective-C class; acts as a proxy for calling Objective-C class methods. Method calls are converted to Objective-C messages on-the-fly -- this is done by replacing underscores in the method name with colons in the selector name, and using the selector and arguments for a call to the low-level objc_msgSend function in the Objective-C runtime. For example, calling `NSDictionary.dictionaryWithObject_forKey_(obj, key)` (Python) is translated to `[NSDictionary dictionaryWithObject:obj forKey:key]` (Objective-C). If a method call returns an Objective-C object, it is wrapped in an ObjCInstance, so calls can be chained (ObjCInstance uses an equivalent proxy mechanism).'''
   def __init__(self, name):
      self.ptr = c.objc_getClass(name)
      if self.ptr is None:
         raise ValueError('no Objective-C class named \'%s\' found' % (name,))
      self._as_parameter_ = self.ptr
      self.class_name = name
      self._cached_methods = {}

   def __str__(self):
      return '<ObjCClass: %s>' % (self.class_name,)

   def __eq__(self, other):
      return isinstance(other, ObjCClass) and self.class_name == other.class_name

   def __getattr__(self, attr):
      sel_name = attr.replace('_', ':')
      cached_method = self._cached_methods.get(sel_name, None)
      if not cached_method:
         cached_method = ObjCClassMethod(self, sel_name)
         self._cached_methods[sel_name] = cached_method
      return cached_method
   def __dir__(self):
      m=[k[0] for k in get_class_methods(self)]
      if self.superclass():
         supcls=ObjCClass(ObjCInstance(self.superclass())._get_objc_classname())
         m.extend(supcls.__dir__())
      return m

class ObjCIterator (object):
   '''Wrapper for an NSEnumerator object -- this is used for supporting `for ... in` iteration for Objective-C collection types (NSArray, NSDictionary, NSSet).'''
   def __init__(self, obj):
      self.enumerator = obj.objectEnumerator()

   def __iter__(self):
      return self

   def next(self):
      next_obj = self.enumerator.nextObject()
      if not next_obj:
         raise StopIteration()
      return next_obj

class ObjCInstance (object):
   '''Wrapper for a pointer to an Objective-C instance; acts as a proxy for sending messages to the object. Method calls are converted to Objective-C messages on-the-fly -- this is done by replacing underscores in the method name with colons in the selector name, and using the selector and arguments for a call to the low-level objc_msgSend function in the Objective-C runtime. For example, calling `obj.setFoo_withBar_(foo, bar)` (Python) is translated to `[obj setFoo:foo withBar:bar]` (Objective-C). If a method call returns an Objective-C object, it is also wrapped in an ObjCInstance, so calls can be chained.'''
   def __init__(self, ptr):
      if hasattr(ptr,'_objc_ptr'):
         self.ptr=ptr._objc_ptr
      else:
         self.ptr = ptr
      self._as_parameter_ = ptr
      self._cached_methods = {}
      if ptr:
         # Retain the ObjC object, so it doesn't get freed while a pointer to it exists:
         self.retain()

   def __str__(self):
      c.objc_msgSend.argtypes = [c_void_p, c_void_p]
      c.objc_msgSend.restype = c_void_p
      desc = c.objc_msgSend(self.ptr, sel('description'))
      c.objc_msgSend.argtypes = [c_void_p, c_void_p]
      c.objc_msgSend.restype = c_char_p
      desc_str = c.objc_msgSend(desc, sel('UTF8String'))
      return desc_str

   def _get_objc_classname(self):
      return c.class_getName(c.object_getClass(self.ptr))

   def __repr__(self):
      return '<%s: %s>' % (self._get_objc_classname(), str(self))

   def __eq__(self, other):
      return isinstance(other, ObjCInstance) and self.ptr == other.ptr

   def __hash__(self):
      return hash(self.ptr)

   def __iter__(self):
      if any(self.isKindOfClass_(c) for c in (NSArray, NSDictionary, NSSet)):
         return ObjCIterator(self)
      raise TypeError('%s is not iterable' % (self._get_objc_classname(),))

   def __nonzero__(self):
      try:
         return len(self) != 0
      except TypeError:
         return self.ptr != None

   def __len__(self):
      if hasattr(self,'count'):
         return self.count()
      raise TypeError('object of type \'%s\' has no len()' % (self._get_objc_classname(),))

   def __getitem__(self, key):
      if hasattr(self,'objectAtIndex_'):
         if not isinstance(key, (int, long)):
            raise TypeError('array indices must be integers not %s' % (type(key),))
         array_length = self.count()
         if key < 0:
            # a[-1] is equivalent to a[len(a) - 1]
            key = array_length + key
         if key < 0 or key >= array_length:
            raise IndexError('array index out of range')
         return self.objectAtIndex_(key)
      elif hasattr(self,'objectForKey_'):
         # allow to use Python strings as keys, convert to NSString implicitly:
         ns_key = ns(key)
         # NOTE: Unlike Python dicts, NSDictionary returns nil (None) for keys that don't exist.
         return self.objectForKey_(ns_key)
      raise TypeError('%s does not support __getitem__' % (self._get_objc_classname(),))

   def __delitem__(self, key):
      if hasattr(self,'removeObjectAtIndex'):
         if not isinstance(key, (int, long)):
            raise TypeError('array indices must be integers not %s' % (type(key),))
         array_length = self.count()
         if key < 0:
            # a[-1] is equivalent to a[len(a) - 1]
            key = array_length + key
         if key < 0 or key >= array_length:
            raise IndexError('array index out of range')
         self.removeObjectAtIndex_(key)
      elif hasattr(self,'removeObjectForKey'):
         ns_key = ns(key)
         return self.removeObjectForKey_(ns_key)
      else:
         raise TypeError('%s does not support __delitem__' % (self._get_objc_classname(),))

   def __setitem__(self, key, value):
      if hasattr(self,'replaceObjectAtIndex_withObject_'):
         if not isinstance(key, (int, long)):
            raise TypeError('array indices must be integers not %s' % (type(key),))
         array_length = self.count()
         if key < 0:
            # a[-1] is equivalent to a[len(a) - 1]
            key = array_length + key
         if key < 0 or key >= array_length:
            raise IndexError('array index out of range')
         self.replaceObjectAtIndex_withObject_(key, ns(value))
      elif hasattr(self, 'setObject_forKey_'):
         self.setObject_forKey_(ns(value), ns(key))
      else:
         raise TypeError('%s does not support __setitem__' % (self._get_objc_classname(),))

   def __getattr__(self, attr):
      sel_name = attr.replace('_', ':')
      cached_method = self._cached_methods.get(sel_name, None)
      if not cached_method:
         cached_method = ObjCInstanceMethod(self, sel_name)
         self._cached_methods[sel_name] = cached_method
      return cached_method

   def __del__(self):
      # Release the ObjC object's memory:
      self.release()
   def __dir__(self):
      cls=ObjCClass(self._get_objc_classname())
      m=[k[0] for k in get_methods(cls)]
      #m.extend([k[0] for k in get_class_methods(cls)])
      if self.superclass():
         supcls=ObjCInstance(self.superclass())
         m.extend(supcls.__dir__())
      return m
def _get_possible_selector_names(method_name):
   import itertools
   return [''.join([x+y for x, y in itertools.izip_longest(method_name.split('_'), s, fillvalue='')]) for s in [''.join(x) for x in itertools.product(':_', repeat=len(method_name.split('_'))-1)]]

class ObjCClassMethod (object):
	'''Wrapper for an Objective-C class method. ObjCClass generates these objects automatically when accessing an attribute, you typically don't need use this class directly.'''
	def __init__(self, cls, method_name):
		self.cls = cls
		
		self.sel_name = method_name.replace('_', ':')
		method = class_getClassMethod(self.cls.ptr, sel(self.sel_name))
		if not method:
			# Couldn't find a method, try all combinations of underscores and colons...
			# For selectors that contain underscores, the mapping from Python method name to selector name is ambiguous.
			possible_selector_names = _get_possible_selector_names(method_name)
			for possible_sel_name in possible_selector_names:
				method = class_getClassMethod(self.cls.ptr, sel(possible_sel_name))
				if method:
					self.sel_name = possible_sel_name
					break
		if method:
			self.method = method
		else:
			raise RuntimeError('No class method found for selector "%s"' % (self.sel_name))
	
	def __call__(self, *args, **kwargs):
		type_encoding = c.method_getTypeEncoding(self.method)
		type_parser = kwargs.get('type_parser', parse_types)
		restype, argtypes = type_parser(type_encoding)
		c.objc_msgSend.argtypes = argtypes
		c.objc_msgSend.restype = restype
		res = c.objc_msgSend(self.cls.ptr, sel(self.sel_name), *args)
		if res and type_encoding[0] == '@':
			return ObjCInstance(res)
		return res
		
class ObjCInstanceMethod (object):
	'''Wrapper for an Objective-C instance method. ObjCInstance generates these objects automatically when accessing an attribute, you typically don't need to use this class directly.'''
	def __init__(self, obj, method_name):
		self.obj = obj
		objc_class = object_getClass(obj.ptr)
		
		self.sel_name = method_name.replace('_', ':')
		method = class_getInstanceMethod(objc_class, sel(self.sel_name))
		if not method:
			# Couldn't find a method, try all combinations of underscores and colons...
			# For selectors that contain underscores, the mapping from Python method name to selector name is ambiguous.
			possible_selector_names = _get_possible_selector_names(method_name)
			for possible_sel_name in possible_selector_names:
				method = class_getInstanceMethod(objc_class, sel(possible_sel_name))
				if method:
					self.sel_name = possible_sel_name
					break
		if method:
			self.method = method
		else:
			raise RuntimeError('No method found for selector "%s"' % (self.sel_name))
		
	def __call__(self, *args, **kwargs):
		type_encoding = c.method_getTypeEncoding(self.method)
		type_parser = kwargs.get('type_parser', parse_types)
		restype, argtypes = type_parser(type_encoding)
		if restype and issubclass(restype, Structure) and not LP64:
			retval = restype()
			c.objc_msgSend_stret.argtypes = [c_void_p] + argtypes
			c.objc_msgSend_stret.restype = None
			c.objc_msgSend_stret(ctypes.byref(retval), self.obj.ptr, sel(self.sel_name), *args)
			return retval
		else:
			c.objc_msgSend.argtypes = argtypes
			c.objc_msgSend.restype = restype
			res = c.objc_msgSend(self.obj.ptr, sel(self.sel_name), *args)
			if res and type_encoding[0] == '@':
				if res == self.obj.ptr:
					return self.obj
				# If an object is returned, wrap the pointer in an ObjCInstance:
				return ObjCInstance(res)
			return res

#Some commonly-used Foundation classes:
NSDictionary = ObjCClass('NSDictionary')
NSMutableDictionary = ObjCClass('NSMutableDictionary')
NSArray = ObjCClass('NSArray')
NSMutableArray = ObjCClass('NSMutableArray')
NSSet = ObjCClass('NSSet')
NSMutableSet = ObjCClass('NSMutableSet')
NSString = ObjCClass('NSString')
NSMutableString = ObjCClass('NSMutableString')
NSData = ObjCClass('NSData')
NSMutableData = ObjCClass('NSMutableData')
NSNumber = ObjCClass('NSNumber')
NSURL = ObjCClass('NSURL')
NSEnumerator = ObjCClass('NSEnumerator')

def ns(py_obj):
   '''Convert common Python objects to their ObjC equivalents, i.e. str => NSString, int/float => NSNumber, list => NSMutableArray, dict => NSMutableDictionary, bytearray => NSData, set => NSMutableSet. Nested structures (list/dict/set) are supported. If an object is already an instance of ObjCInstance, it is left untouched.
'''
   if isinstance(py_obj, ObjCInstance):
      return py_obj
   if isinstance(py_obj, str):
      return NSString.stringWithUTF8String_(py_obj)
   if isinstance(py_obj, unicode):
      return NSString.stringWithUTF8String_(py_obj.encode('utf-8'))
   elif isinstance(py_obj, bytearray):
      return NSData.dataWithBytes_length_(str(py_obj), len(py_obj))
   elif isinstance(py_obj, int):
      return NSNumber.numberWithInt_(py_obj)
   elif isinstance(py_obj, float):
      return NSNumber.numberWithDouble_(py_obj)
   elif isinstance(py_obj, bool):
      return NSNumber.numberWithBool_(py_obj)
   elif isinstance(py_obj, list):
      arr = NSMutableArray.array()
      for obj in py_obj:
         arr.addObject_(ns(obj))
      return arr
   elif isinstance(py_obj, set):
      s = NSMutableSet.set()
      for obj in py_obj:
         s.addObject_(ns(obj))
      return s
   elif isinstance(py_obj, dict):
      dct = NSMutableDictionary.dictionary()
      for key, value in py_obj.iteritems():
         dct.setObject_forKey_(ns(value), ns(key))
      return dct

def nsurl(url_or_path):
   if not isinstance(url_or_path, basestring):
      raise TypeError('expected a string')
   if ':' in url_or_path:
      return NSURL.URLWithString_(ns(url_or_path))
   return NSURL.fileURLWithPath_(ns(url_or_path))