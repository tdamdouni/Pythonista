# coding: utf-8

# https://github.com/jsbain/objc_hacks/blob/master/objcnew.py

try:
	import ctypes
except ImportError:
	raise NotImplementedError("objc_util requires ctypes, which doesn't seem to be available.")

from ctypes import Structure, sizeof, byref, cdll, pydll, c_void_p, c_char, c_byte, c_char_p, c_double, c_float, c_int, c_longlong, c_short, c_bool, c_long, c_int32, c_ubyte, c_uint, c_ushort, c_ulong, c_ulonglong, POINTER, pointer
import re
import sys
import os
import itertools
import ui
import weakref
import string
import pyparsing as pp


LP64 = (sizeof(c_void_p) == 8)

_retained_globals = []
_cached_classes = {}
_cached_instances = weakref.WeakValueDictionary()

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

class_copyMethodList = c.class_copyMethodList
class_copyMethodList.restype = ctypes.POINTER(c_void_p)
class_copyMethodList.argtypes = [c_void_p, ctypes.POINTER(ctypes.c_uint)]

method_getName = c.method_getName
method_getName.restype = c_void_p
method_getName.argtypes = [c_void_p]

class objc_method_description (Structure):
	_fields_ = [('sel', c_void_p), ('types', c_char_p)]

objc_getProtocol = c.objc_getProtocol
objc_getProtocol.restype = c_void_p
objc_getProtocol.argtypes = [c_char_p]

protocol_getMethodDescription = c.protocol_getMethodDescription
protocol_getMethodDescription.restype = objc_method_description
protocol_getMethodDescription.argtypes = [c_void_p, c_void_p, c_bool, c_bool]

objc_msgSend = c.objc_msgSend
if not LP64:
	objc_msgSend_stret = c.objc_msgSend_stret

free = c.free
free.argtypes = [c_void_p]
free.restype = None

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

class CGAffineTransform (Structure):
	_fields_ = [('a', CGFloat), ('b', CGFloat), ('c', CGFloat), ('d', CGFloat), ('tx', CGFloat), ('ty', CGFloat)]

class UIEdgeInsets (Structure):
	_fields_ = [('top', CGFloat), ('left', CGFloat), ('bottom', CGFloat), ('right', CGFloat)]

class NSRange (Structure):
	_fields_ = [('location', NSUInteger), ('length', NSUInteger)]

# These are used by show():
UIGraphicsBeginImageContext = c.UIGraphicsBeginImageContext
UIGraphicsBeginImageContext.restype = None
UIGraphicsBeginImageContext.argtypes = [CGSize]
UIGraphicsBeginImageContextWithOptions = c.UIGraphicsBeginImageContextWithOptions
UIGraphicsBeginImageContextWithOptions.restype = None
UIGraphicsBeginImageContextWithOptions.argtypes = [CGSize, c_bool, CGFloat]
UIGraphicsEndImageContext = c.UIGraphicsBeginImageContext
UIGraphicsEndImageContext.restype = None
UIGraphicsEndImageContext.argtypes = []
UIGraphicsGetImageFromCurrentImageContext = c.UIGraphicsGetImageFromCurrentImageContext
UIGraphicsGetImageFromCurrentImageContext.restype = c_void_p
UIGraphicsGetImageFromCurrentImageContext.argtypes = []
UIImagePNGRepresentation = c.UIImagePNGRepresentation
UIImagePNGRepresentation.restype = c_void_p
UIImagePNGRepresentation.argtypes = [c_void_p]
UIGraphicsGetCurrentContext = c.UIGraphicsGetCurrentContext
UIGraphicsGetCurrentContext.restype = c_void_p
UIGraphicsGetCurrentContext.argtypes = []

# c.f. https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtTypeEncodings.html
type_encodings = {'c': c_byte, 'i': c_int, 's': c_short, 'l': c_int32, 'q': c_longlong,
	'C': c_ubyte, 'I': c_uint, 'S': c_ushort, 'L': c_ulong, 'Q': c_ulonglong,
	'f': c_float, 'd': c_double, 'B': c_bool, 'v': None, '*': c_char_p,
	'@': c_void_p, '#': c_void_p, ':': c_void_p,
	'{CGPoint}': CGPoint, '{CGSize}': CGSize, '{CGRect}': CGRect, '{CGVector}': CGVector,
	'{CGAffineTransform}': CGAffineTransform, '{UIEdgeInsets}': UIEdgeInsets, '{_NSRange}': NSRange,
	'?': c_void_p, '@?': c_void_p
}

def split_encoding(encoding):
	# This function is mostly copied from pybee's rubicon.objc
	# (https://github.com/pybee/rubicon-objc)
	# License: https://github.com/pybee/rubicon-objc/blob/master/LICENSE
	type_encodings = []
	braces, brackets = 0, 0
	typecode = ''
	for c in encoding:
		if c == '{':
			if typecode and typecode[-1:] != '^' and braces == 0 and brackets == 0:
				type_encodings.append(typecode)
				typecode = ''
			typecode += c
			braces += 1
		elif c == '}':
			typecode += c
			braces -= 1
		elif c == '[':
			if typecode and typecode[-1:] != '^' and braces == 0 and brackets == 0:
				type_encodings.append(typecode)
				typecode = ''
			typecode += c
			brackets += 1
		elif c == ']':
			typecode += c
			brackets -= 1
		elif braces or brackets:
			typecode += c
		elif c in string.digits:
			pass
		elif c in 'rnNoORV':
			pass
		elif c in '^cislqCISLQfdBv*@#:b?':
			if c == '?' and typecode[-1:] == '@':
				typecode += c
			elif typecode and typecode[-1:] == '^':
				typecode += c
			else:
				if typecode:
					type_encodings.append(typecode)
				typecode = c
	if typecode:
		type_encodings.append(typecode)
	return type_encodings


def struct_from_tuple(cls, t):
	args = []
	for i, field_value in enumerate(t):
		if isinstance(field_value, tuple):
			args.append(struct_from_tuple(cls._fields_[i][1], field_value))
		else:
			args.append(field_value)
	return cls(*args)
	
def _struct_class_from_fields(fields):
	class AnonymousStructure (Structure):
		from_tuple = classmethod(struct_from_tuple)
	struct_fields = []
	for i, field in enumerate(fields):
		if isinstance(field, tuple):
			struct_fields.append(field)
		else:
			struct_fields.append((string.lowercase[i], _struct_class_from_fields(field)))
			i += 1
	AnonymousStructure._fields_ = struct_fields
	return AnonymousStructure

def _list_to_fields(result):
	fields = []
	i = 0
	if isinstance(result, basestring):
		for char in split_encoding(result):
			c_type = parse_types(char)[0]
			fields.append((string.lowercase[i], c_type))
			i += 1
	else:
		if len(result) == 1:
			return _list_to_fields(result[0])
		for r in result:
			fields.append(_list_to_fields(r))
	return fields

def _result_to_list(result):
	struct_result = []
	for member in result:
		if isinstance(member, basestring):
			struct_result.append(member)
		else:
			struct_result.append(_result_to_list([member[2]]))
	return struct_result

_enclosed = pp.Forward()
_nested_curlies = pp.nestedExpr('{', '}', content=_enclosed)
_enclosed << (pp.Word(pp.alphas + '?_' + pp.nums) | '=' | _nested_curlies)

def parse_struct(encoding):
	comps = _enclosed.parseString(encoding).asList()[0]
	struct_name = comps[0]
	struct_members = comps[2:]
	fields = _list_to_fields(_result_to_list(struct_members))
	struct_class = _struct_class_from_fields(fields)
	struct_class.__name__ = (struct_name + '_Structure').replace('?', '_')
	return struct_class

_cached_parse_types_results = {}

def parse_types(type_encoding):
	'''Take an Objective-C type encoding string and convert it to a tuple of (restype, argtypes) appropriate for objc_msgSend()'''
	cached_result = _cached_parse_types_results.get(type_encoding)
	if cached_result:
		return cached_result
	def get_type_for_code(enc_str):
		if enc_str.startswith('{'):
			struct_name = enc_str[0:enc_str.find('=')] + '}'
			if struct_name in type_encodings:
				return type_encodings[struct_name]
			else:
				return parse_struct(enc_str)
		if enc_str[0] in 'rnNoORV': #const, in, inout... don't care about these
			enc_str = enc_str[1:]
		if enc_str[0] == '^':
			if re.match(r'\^\{\w+=\}', enc_str):
				return c_void_p # pointer to opaque type, e.g. CGPathRef, CGImageRef...
			else:
				return POINTER(get_type_for_code(enc_str[1:]))
		if enc_str[0] == '[': #array
			return c_void_p
		try:
			t = type_encodings[enc_str]
			return t
		except KeyError:
			raise NotImplementedError('Unsupported type encoding (%s)' % (enc_str,))
	encoded_types = filter(lambda x: bool(x), split_encoding(type_encoding))
	encoded_argtypes = encoded_types[3:]
	argtypes = [get_type_for_code(x) for x in encoded_argtypes]
	restype = get_type_for_code(encoded_types[0])
	cached_result = (restype, [c_void_p, c_void_p] + argtypes, encoded_argtypes)
	_cached_parse_types_results[type_encoding] = cached_result
	return cached_result

def sel(sel_name):
	'''Convenience function to convert a string to a selector'''
	return sel_registerName(sel_name)

class ObjCClass (object):
	'''Wrapper for a pointer to an Objective-C class; acts as a proxy for calling Objective-C class methods. Method calls are converted to Objective-C messages on-the-fly -- this is done by replacing underscores in the method name with colons in the selector name, and using the selector and arguments for a call to the low-level objc_msgSend function in the Objective-C runtime. For example, calling `NSDictionary.dictionaryWithObject_forKey_(obj, key)` (Python) is translated to `[NSDictionary dictionaryWithObject:obj forKey:key]` (Objective-C). If a method call returns an Objective-C object, it is wrapped in an ObjCInstance, so calls can be chained (ObjCInstance uses an equivalent proxy mechanism).'''
	def __new__(cls, name):
		# Memoize classes by name (get identical object every time):
		cached_class = _cached_classes.get(name)
		if cached_class:
			return cached_class
		cached_class = super(ObjCClass, cls).__new__(cls)
		_cached_classes[name] = cached_class
		return cached_class
	
	def __init__(self, name):
		self.ptr = objc_getClass(name)
		if self.ptr is None:
			raise ValueError('no Objective-C class named \'%s\' found' % (name,))
		self._as_parameter_ = self.ptr
		self.class_name = name
		self._cached_methods = weakref.WeakValueDictionary()
	
	def __str__(self):
		return '<ObjCClass: %s>' % (self.class_name,)
	
	def __eq__(self, other):
		return isinstance(other, ObjCClass) and self.class_name == other.class_name
	
	def __getattr__(self, attr):
		cached_method = self._cached_methods.get(attr, None)
		if not cached_method:
			cached_method = ObjCClassMethod(self, attr)
			self._cached_methods[attr] = cached_method
		return cached_method
	
	def __dir__(self):
		objc_class_ptr = object_getClass(self.ptr)
		py_methods = []
		while objc_class_ptr is not None:
			num_methods = c_uint(0)
			method_list_ptr = class_copyMethodList(objc_class_ptr, byref(num_methods))
			for i in xrange(num_methods.value):
				selector = method_getName(method_list_ptr[i])
				sel_name = sel_getName(selector)
				py_method_name = sel_name.replace(':', '_')
				if '.' not in py_method_name:
					py_methods.append(py_method_name)
			free(method_list_ptr)
			# Walk up the class hierarchy to add methods from superclasses:
			objc_class_ptr = class_getSuperclass(objc_class_ptr)
			if objc_class_ptr == object_getClass(NSObject):
				# Don't list all methods from NSObject (too much cruft from categories)
				py_methods += NSObject_class_methods
				break
		py_methods = sorted(set(py_methods))
		return py_methods

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
	
	def __new__(cls, ptr):
		# If there is already an instance that wraps this pointer, return the same object...
		# This makes it a little easier to put auxiliary data into the instance (e.g. to use in an ObjC callback)
		# Note however that a new instance may be created for the same underlying ObjC object if the last instance gets garbage-collected.
		if isinstance(ptr, ui.View):
			ptr = ptr._objc_ptr
		if isinstance(ptr, ObjCInstance):
			return ptr
		if isinstance(ptr, c_void_p):
			ptr = ptr.value
		cached_instance = _cached_instances.get(ptr)
		if cached_instance:
			return cached_instance
		objc_instance = super(ObjCInstance, cls).__new__(cls)
		_cached_instances[ptr] = objc_instance
		if isinstance(ptr, ui.View):
			ptr = ptr._objc_ptr
		objc_instance.ptr = ptr
		objc_instance._as_parameter_ = ptr
		objc_instance._cached_methods = weakref.WeakValueDictionary()
		objc_instance.weakrefs = weakref.WeakValueDictionary()
		if ptr:
			# Retain the ObjC object, so it doesn't get freed while a pointer to it exists:
			objc_instance.retain(restype=c_void_p, argtypes=[])
		return objc_instance
		
	def __str__(self):
		objc_msgSend = c['objc_msgSend']
		objc_msgSend.argtypes = [c_void_p, c_void_p]
		objc_msgSend.restype = c_void_p
		desc = objc_msgSend(self.ptr, sel('description'))
		objc_msgSend.argtypes = [c_void_p, c_void_p]
		objc_msgSend.restype = c_char_p
		desc_str = objc_msgSend(desc, sel('UTF8String'))
		return desc_str
	
	def _get_objc_classname(self):
		return class_getName(object_getClass(self.ptr))
	
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
		if any(self.isKindOfClass_(c) for c in (NSArray, NSDictionary, NSSet)):
			return self.count()
		raise TypeError('object of type \'%s\' has no len()' % (self._get_objc_classname(),))
	
	def __getitem__(self, key):
		if self.isKindOfClass_(NSArray):
			if not isinstance(key, (int, long)):
				raise TypeError('array indices must be integers not %s' % (type(key),))
			array_length = self.count()
			if key < 0:
				# a[-1] is equivalent to a[len(a) - 1]
				key = array_length + key
			if key < 0 or key >= array_length:
				raise IndexError('array index out of range')
			return self.objectAtIndex_(key)
		elif self.isKindOfClass_(NSDictionary):
			# allow to use Python strings as keys, convert to NSString implicitly:
			ns_key = ns(key)
			# NOTE: Unlike Python dicts, NSDictionary returns nil (None) for keys that don't exist.
			return self.objectForKey_(ns_key)
		raise TypeError('%s does not support __getitem__' % (self._get_objc_classname(),))
	
	def __delitem__(self, key):
		if self.isKindOfClass_(NSMutableArray):
			if not isinstance(key, (int, long)):
				raise TypeError('array indices must be integers not %s' % (type(key),))
			array_length = self.count()
			if key < 0:
				# a[-1] is equivalent to a[len(a) - 1]
				key = array_length + key
			if key < 0 or key >= array_length:
				raise IndexError('array index out of range')
			self.removeObjectAtIndex_(key)
		elif self.isKindOfClass_(NSMutableDictionary):
			ns_key = ns(key)
			return self.removeObjectForKey_(ns_key)
		else:
			raise TypeError('%s does not support __delitem__' % (self._get_objc_classname(),))
	
	def __setitem__(self, key, value):
		if self.isKindOfClass_(NSMutableArray):
			if not isinstance(key, (int, long)):
				raise TypeError('array indices must be integers not %s' % (type(key),))
			array_length = self.count()
			if key < 0:
				# a[-1] is equivalent to a[len(a) - 1]
				key = array_length + key
			if key < 0 or key >= array_length:
				raise IndexError('array index out of range')
			self.replaceObjectAtIndex_withObject_(key, ns(value))
		elif self.isKindOfClass_(NSMutableDictionary):
			self.setObject_forKey_(ns(value), ns(key))
		else:
			raise TypeError('%s does not support __setitem__' % (self._get_objc_classname(),))
						
	def __getattr__(self, attr):
		cached_method = self._cached_methods.get(attr, None)
		if not cached_method:
			cached_method = ObjCInstanceMethod(self, attr)
			self._cached_methods[attr] = cached_method
		return cached_method

	def __dir__(self):
		objc_class_ptr = object_getClass(self.ptr)
		py_methods = []
		while objc_class_ptr is not None:
			num_methods = c_uint(0)
			method_list_ptr = class_copyMethodList(objc_class_ptr, byref(num_methods))
			for i in xrange(num_methods.value):
				selector = method_getName(method_list_ptr[i])
				sel_name = sel_getName(selector)
				py_method_name = sel_name.replace(':', '_')
				if '.' not in py_method_name:
					py_methods.append(py_method_name)
			free(method_list_ptr)
			# Walk up the class hierarchy to add methods from superclasses:
			objc_class_ptr = class_getSuperclass(objc_class_ptr)
			if objc_class_ptr == NSObject.ptr:
				# Don't list all NSObject methods (too much cruft from categories...)
				py_methods += NSObject_instance_methods
				break
		return sorted(set(py_methods))

	def __del__(self):
		# Release the ObjC object's memory:
		self.release(restype=None, argtypes=[])

def _get_possible_selector_names(method_name):
	# Generate all possible selector names from a Python method name. For most methods, this isn't necessary,
	# and the selector is generated simply by replacing underscores with colons, but in case the selector also
	# contains underscores, the mapping is ambiguous, so all permutations of colons and underscores need to be checked.
	return [''.join([x+y for x, y in itertools.izip_longest(method_name.split('_'), s, fillvalue='')]) for s in [''.join(x) for x in itertools.product(':_', repeat=len(method_name.split('_'))-1)]]

def _auto_wrap(arg, typecode, argtype):
	'''Helper function for `ObjCInstance/ClassMethod.__call__`'''
	if typecode == '@':
		return ns(arg)
	elif typecode == ':' and isinstance(arg, basestring):
		# if a selector is expected, also allow a string:
		return sel(arg)
	elif issubclass(argtype, Structure) and isinstance(arg, tuple):
		# Automatically convert tuples to structs
		return struct_from_tuple(argtype, arg)
	return arg

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
			self.encoding = method_getTypeEncoding(method)
		else:
			raise RuntimeError('No class method found for selector "%s"' % (self.sel_name))
	
	def __call__(self, *args, **kwargs):
		type_encoding = self.encoding
		try:
			argtypes = kwargs['argtypes']
			restype = kwargs['restype']
			argtypes = [c_void_p, c_void_p] + argtypes
		except KeyError:
			restype, argtypes, argtype_encodings = parse_types(type_encoding)
			if len(args) != len(argtypes) - 2:
				raise TypeError('expected %i arguments, got %i' % (len(argtypes) - 2, len(args)))
			# Automatically convert Python strings to NSString etc. for object arguments
			# (this is a no-op for arguments that are already `ObjCInstance` objects):
			args = tuple(_auto_wrap(a, argtype_encodings[i], argtypes[i+2]) for i, a in enumerate(args))
		objc_msgSend = c['objc_msgSend']
		objc_msgSend.argtypes = argtypes
		objc_msgSend.restype = restype
		res = objc_msgSend(self.cls, sel(self.sel_name), *args)
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
			self.encoding = method_getTypeEncoding(method) 
		else:
			raise RuntimeError('No method found for selector "%s"' % (self.sel_name))
	
	def __call__(self, *args, **kwargs):
		type_encoding = self.encoding
		try:
			argtypes = kwargs['argtypes']
			restype = kwargs['restype']
			argtypes = [c_void_p, c_void_p] + argtypes
		except KeyError:
			restype, argtypes, argtype_encodings = parse_types(type_encoding)
			if len(args) != len(argtypes) - 2:
				raise TypeError('expected %i arguments, got %i' % (len(argtypes) - 2, len(args)))
			# Automatically convert Python strings to NSString etc. for object arguments
			# (this is a no-op for arguments that are already `ObjCInstance` objects):
			args = tuple(_auto_wrap(a, argtype_encodings[i], argtypes[i+2]) for i, a in enumerate(args))
			
		if restype and issubclass(restype, Structure) and not LP64:
			retval = restype()
			objc_msgSend_stret = c['objc_msgSend_stret']
			objc_msgSend_stret.argtypes = [c_void_p] + argtypes
			objc_msgSend_stret.restype = None
			objc_msgSend_stret(byref(retval), self.obj.ptr, sel(self.sel_name), *args)
			return retval
		else:
			# NOTE: In order to be thread-safe, we need a "private" handle for objc_msgSend(...).
			#       Otherwise, a different thread could modify argtypes/restypes before the call is made...
			objc_msgSend = c['objc_msgSend']
			objc_msgSend.argtypes = argtypes
			objc_msgSend.restype = restype
			
			res = objc_msgSend(self.obj.ptr, sel(self.sel_name), *args)
			if res and type_encoding[0] == '@':
				# If an object is returned, wrap the pointer in an ObjCInstance:
				if res == self.obj.ptr:
					return self.obj
				return ObjCInstance(res)
			if restype == c_void_p and isinstance(res, int):
				res = c_void_p(res)
			return res

#Some commonly-used Foundation/UIKit classes:
NSObject = ObjCClass('NSObject')
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
NSThread = ObjCClass('NSThread')

UIColor = ObjCClass('UIColor')
UIImage = ObjCClass('UIImage')
UIBezierPath = ObjCClass('UIBezierPath')
UIApplication = ObjCClass('UIApplication')
UIView = ObjCClass('UIView')

# These are hard-coded for __dir__ (listing all NSObject methods dynamically would add tons of cruft from categories)
# NOTE: This only includes *commonly-used* methods (a lot of this is pretty low-level runtime stuff that isn't needed
#       very often. It can still be listed when calling dir() on an actual instance of NSObject)
NSObject_class_methods = ['alloc', 'new', 'superclass', 'isSubclassOfClass_', 'instancesRespondToSelector_', 'description', 'cancelPreviousPerformRequestsWithTarget_', 'cancelPreviousPerformRequestsWithTarget_selector_object_']
NSObject_instance_methods = ['init', 'copy', 'mutableCopy', 'dealloc', 'performSelector_withObject_afterDelay_', 'performSelectorOnMainThread_withObject_waitUntilDone_', 'performSelectorInBackground_withObject_']

class _block_descriptor (Structure):
	_fields_ = [('reserved', c_ulong), ('size', c_ulong), ('copy_helper', c_void_p), ('dispose_helper', c_void_p), ('signature', c_char_p)]

class ObjCBlock (object):
	def __init__(self, func, restype=None, argtypes=None):
		if not callable(func):
			raise TypeError('%s is not callable' % func)
		if argtypes is None:
			argtypes = []
		InvokeFuncType = ctypes.CFUNCTYPE(restype, *argtypes)
		class block_literal(Structure):
			_fields_ = [('isa', c_void_p), ('flags', c_int), ('reserved', c_int), ('invoke', InvokeFuncType), ('descriptor', _block_descriptor)]
		block = block_literal()
		block.flags = (1<<28)
		block.invoke = InvokeFuncType(func)
		block.isa = ObjCClass('__NSGlobalBlock__').ptr
		self._as_parameter_ = block if LP64 else byref(block)
	
	@classmethod
	def from_param(cls, param):
		if isinstance(param, ObjCBlock) or param is None:
			return param
		elif callable(param):
			block = ObjCBlock(param)
			# Put a reference to the block into the function, so it doesn't get deallocated prematurely...
			param._block = block
			return block
		raise TypeError('cannot convert parameter to block')
	
	def __call__(self, *args):
		return self.func(*args)

type_encodings['@?'] = ObjCBlock


def ns(py_obj):
	'''Convert common Python objects to their ObjC equivalents, i.e. str => NSString, int/float => NSNumber, list => NSMutableArray, dict => NSMutableDictionary, bytearray => NSData, set => NSMutableSet. Nested structures (list/dict/set) are supported. If an object is already an instance of ObjCInstance, it is left untouched.
		'''
	if isinstance(py_obj, ObjCInstance):
		return py_obj
	if isinstance(py_obj, c_void_p):
		return ObjCInstance(py_obj)
	if isinstance(py_obj, ui.View):
		return ObjCInstance(py_obj)
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

def retain_global(obj):
	'''Keep an object alive'''
	_retained_globals.append(obj)

def release_global(obj):
	try:
		_retained_globals.remove(obj)
	except ValueError:
		pass

def OMMainThreadDispatcher_invoke_imp(self, cmd):
	self_instance = ObjCInstance(self)
	func = self_instance.func
	args = self_instance.args
	kwargs = self_instance.kwargs
	retval = func(*args, **kwargs)
	self_instance.retval = retval

try:
	OMMainThreadDispatcher = ObjCClass('OMMainThreadDispatcher')
except ValueError:
	IMPTYPE = ctypes.CFUNCTYPE(None, c_void_p, c_void_p)
	imp = IMPTYPE(OMMainThreadDispatcher_invoke_imp)
	retain_global(imp)
	NSObject = ObjCClass('NSObject')
	class_ptr = objc_allocateClassPair(NSObject.ptr, 'OMMainThreadDispatcher', 0)
	class_addMethod(class_ptr, sel('invoke'), imp, 'v16@0:0')
	objc_registerClassPair(class_ptr)
	OMMainThreadDispatcher = ObjCClass('OMMainThreadDispatcher')

def on_main_thread(func):
	if not callable(func):
		raise TypeError('expected a callable')
	def new_func(*args, **kwargs):
		if NSThread.isMainThread(restype=c_bool, argtypes=[]):
			return func(*args, **kwargs)
		dispatcher = OMMainThreadDispatcher.new()
		dispatcher.func = func
		dispatcher.args = args
		dispatcher.kwargs = kwargs
		dispatcher.retval = None
		dispatcher.performSelectorOnMainThread_withObject_waitUntilDone_(sel('invoke'), None, True)
		retval = dispatcher.retval
		dispatcher.release()
		return retval
	return new_func

def _add_method(method, class_ptr, superclass, basename, protocols, is_classmethod=False):
	'''Helper function for create_objc_class, don't use directly (will usually crash)!'''
	if hasattr(method, 'selector'):
		sel_name = method.selector
	else:
		method_name = method.__name__
		if method_name.startswith(basename + '_'):
			method_name = method_name[len(basename)+1:]
		sel_name = method_name.replace('_', ':')
	type_encoding = None
	if hasattr(method, 'encoding'):
		type_encoding = method.encoding
	else:
		# Try to derive type encoding from superclass...
		if is_classmethod:
			superclass_method = class_getClassMethod(superclass, sel(sel_name))
		else:
			superclass_method = class_getInstanceMethod(superclass, sel(sel_name))
		if superclass_method:
			type_encoding = method_getTypeEncoding(superclass_method)
		else:
			# Try to find a matching method in one of the protocols
			for protocol_name in protocols:
				protocol = objc_getProtocol(protocol_name)
				if protocol:
					# Try optional method first...
					method_desc = protocol_getMethodDescription(protocol, sel(sel_name), False, True)
					if not method_desc:
						#... then required method
						method_desc = protocol_getMethodDescription(protocol, sel(sel_name), True, True)
					if method_desc:
						type_encoding = method_desc.types
						break
		if not type_encoding:
			# Fall back to "action" type encoding as the default, i.e. void return type, all arguments are objects...
			num_args = len(re.findall(':', sel_name))
			type_encoding = 'v%i@0:8%s' % (sizeof(c_void_p) * (num_args + 2), ''.join('@%i' % ((i+2) * sizeof(c_void_p),) for i in xrange(num_args)))
			
	if hasattr(method, 'restype') and hasattr(method, 'argtypes'):
		restype = method.restype
		argtypes = [c_void_p, c_void_p] + method.argtypes
	else:
		parsed_types = parse_types(type_encoding)
		restype = parsed_types[0]
		argtypes = parsed_types[1]
	IMPTYPE = ctypes.CFUNCTYPE(restype, *argtypes)
	imp = IMPTYPE(method)
	retain_global(imp)
	class_addMethod(class_ptr, sel(sel_name), imp, type_encoding)

def create_objc_class(name, superclass=NSObject, methods=[], classmethods=[], protocols=[], debug=True):
	'''Create and return a new Objective-C class'''
	basename = name
	if debug:
		# When debug is True (the default) and a class with the given name already exists in the runtime, append an incrementing numeric suffix, until a class name is found that doesn't exist yet. While this does leak some memory, it makes development much easier. Note however that the returned class may not have the name you passed in (use the return value directly instead of relying on the name)
		suffix = 1
		while True:
			try:
				existing_class = ObjCClass(name)
				suffix += 1
				name = '%s_%i' % (basename, suffix)
			except ValueError:
				break
	else:
		# When debug is False, assume that any class is created only once, and return an existing class with the given name. Note that this ignores all other parameters. This is intended to avoid memory leaks when the class definition doesn't change anymore.
		try:
			existing_class = ObjCClass(basename)
			return existing_class
		except ValueError:
			pass
	class_ptr = objc_allocateClassPair(superclass, name, 0)
	
	for method in methods:
		_add_method(method, class_ptr, superclass, basename, protocols)
	
	objc_registerClassPair(class_ptr)
	
	for method in classmethods:
		metaclass = object_getClass(class_ptr)
		super_metaclass = object_getClass(class_getSuperclass(class_ptr))
		_add_method(method, metaclass, super_metaclass, basename, [], True)
	return ObjCClass(name)