# coding: utf-8

# https://gist.github.com/filippocld/605d36756c57d051a612

from __future__ import print_function
from objc_util import *
import ctypes
import webbrowser

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

def get_properties(objc_class):
	'''useless... selectors seem to be props and vice versa?'''
	free = c.free
	free.argtypes = [c_void_p]
	free.restype = None

	class_copyPropertyList = c.class_copyMethodList
	class_copyPropertyList.restype = ctypes.POINTER(c_void_p)
	class_copyPropertyList.argtypes = [c_void_p, ctypes.POINTER(ctypes.c_uint)]

	property_getName = c.property_getName
	property_getName.restype = c_char_p
	property_getName.argtypes = [c_void_p]
	py_properties = []
	num_props = c_uint(0)
	prop_list_ptr = class_copyPropertyList(objc_class.ptr, ctypes.byref(num_props))
	try:
		for i in xrange(num_props.value):
			py_properties.append(property_getName(prop_list_ptr[i]))
	finally:
		free(prop_list_ptr)
	return py_properties


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
def print_methods(clsname,show_docs=True,print_private=True):
	'''Prints all availabe classes and instances for a class and shows the docs'''
	cls=ObjCClass(clsname)
	console.set_color(1,0,0)
	print(clsname)
	print('Class Methods______')
	console.set_color(0,0,0)
	m=get_class_methods(cls)
	print('\n'.join([(k[1]+' ' +k[0]+'( '+', '.join(k[2])+' )') for k in m if not k[0].startswith('_')]))
	if print_private:
		print('\n'.join([(k[1]+' ' +k[0]+'( '+', '.join(k[2])+' )') for k in m if k[0].startswith('_')]))
	if show_docs:
		docs(clsname)
	console.set_color(1,0,0)
	print('_______Instance Methods______')
	console.set_color(0,0,0)
	m=get_methods(cls)
	print('\n'.join([(k[1]+'\t' +k[0]+'( '+', '.join(k[2])+' )') for k in m if not k[0].startswith('_')]))
	if print_private:
		print('\n'.join([(k[1]+'\t' +k[0]+'( '+', '.join(k[2])+' )') for k in m if k[0].startswith('_')]))
		
def docs(clsname):
	'''Shows the docs for a class'''
	webbrowser.open('https://developer.apple.com/search/index.php?q='+ clsname +'&platform=iOS')
	
def filter_subviews(view,text=None, objcclasstext=None):
   '''Finds Internal Pythonista views'''
   matching_svs=[]
   sv=view.subviews()
   if sv is None:
      return matching_svs
   for v in sv:
      if objcclasstext and objcclasstext in v._get_objc_classname():
         matching_svs.append(v)
      if text and hasattr(v,'text'):
         if str(v.text()) and text in str(v.text()):
            matching_svs.append(v)
      matching_svs.extend(
       filter_subviews(v, text=text, objcclasstext=objcclasstext))
   return matching_svs
   
def presentUIView(uiview,viewname='',presentmode='panel',remove=False):
	'''Simplifies the presentation of a UIView in a pythonista view'''
	view=ui.View(name=viewname)
	if remove:
		uiview.removeFromSuperview()
	else:
		ObjCInstance(view).addSubview_(uiview)
		view.present(presentmode)
	
def hierarchyview(view):
	'''Prints a tree of subviews'''
	print(str(view.recursiveDescription()))

def tree(view):
	'''Same as hierarchyview'''
	hierarchyview(view)
	
def loadFramework(frameworkpath):
	if frameworkpath.startswith('./'):
		ObjCClass('NSBundle').bundleWithPath_(frameworkpath).load()
	else:
		ObjCClass('NSBundle').bundleWithPath_('/System/Library/Frameworks/'+frameworkpath+'.framework').load()
	
def listFrameworks():
	import os
	frameworks=os.listdir('/System/Library/Frameworks')
	return frameworks
	
def presentUIVC(vc):
	rootvc=ObjCClass('UIApplication').sharedApplication().keyWindow().rootViewController()
	vc.popoverPresentationController().setSourceView_(rootvc.view())
	rootvc.presentViewController_animated_completion_(vc, False, None)
