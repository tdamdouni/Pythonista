from objc_util import *
import weakref
''' Attempt at making more natural objc class in pythonista.

decorate class wth @objc_class.
set superclass and protocols if desired.
decorate objc methods with @objc_method

e.g
@objcclass
class MySearchResultUpdater(object):
	protocol=['UISearchControllerUpdating']
	superclass=NSObject
	def __init_(self):
		self.tv=None
	
	@objcmethod
	def updateSearchResultsForSearchController_(_self,_sel, controller):			
		self=MySearchResultUpdater(_self)   # access self from callback
		tv=self.tv #instance variable!
		if ObjCInstance(controller).active():
			sb=ObjCInstance(controller).searchBar()
			filterTerm=str(sb.text())
			tv.data_source.filter_items(filterTerm)
		else:
			tv.data_source.filter_items('')
			
			
you can access self by using YourClassName(_self), then get to py instance vars, methods, etc

The way this works is that the objc class is created, and attached to the py class.  

'''

def objcmethod(fcn):
	'''fcn gets wrapped as static., and marked so we can find it. 
	'''
	fcn._objcmethod=True
	return staticmethod(fcn)
def get_objc_methods(cls):
	'''find all tagged methods. note, this only works with protocol'''
	methods=[]
	for m in cls.__dict__.values():
		try:
			if m.__func__._objcmethod:
				methods.append(m.__func__)
		except AttributeError:
			pass
	return methods
def objcclass(cls):
	'''decorator which creates an objcclass'''
	methods=get_objc_methods(cls)
	if hasattr(cls,'superclass'):
		superclass=cls.superclass
	else:
		superclass=ObjCClass('NSObject')
	if hasattr(cls,'protocols'):
		protocols=cls.protocols
	else:
		protocols=[]
	
	
	cls._objcclass=create_objc_class(cls.__name__,
				superclass=superclass,
				methods=methods,
				protocols=protocols, debug=True)
	oldinit=cls.__init__

	cls.instances={}
	def __init__(self,*args,**kwargs):
		oldinit(self, *args, **kwargs)
		self.objcinstance=cls._objcclass.new()
		self._objc_ptr=self.objcinstance.ptr
		cls.instances[self.objcinstance.ptr]=weakref.ref(self)
	def get_instance(*args):
		if args:
			return cls.instances[args[0]]()
		else:
			return cls()

	cls.__init__=__init__

	return get_instance

def ObjCBlockWrapper(argtypes=[c_void_p], restype=None):
	def wrapper(func):
		return ObjCBlock(func,argtypes=argtypes,restype=restype)
	return wrapper
'''
@objcclass	
class JBQLDatasource(object):
	protocols=['QLPreviewControllerDataSource',
				'QLPreviewControllerDelegate']
	def __init__(self):
		self.items=[] #list of NSURLs

	@objcmethod
	def numberOfPreviewItemsInPreviewController_(_self,_sel,pvc):
		print('called')
		return len(JBQLDatasource(_self).items)

	@objcmethod
	def previewController_previewItemAtIndex_( _self, _sel, controller, index):
		self=JBQLDatasource(_self)
		return self.items[index].ptr

j=JBQLDatasource()
import os

for f in os.listdir('.'):
	if '.py' not in f:
		j.items.append(nsurl(os.path.abspath(f)))		

pyk=ObjCClass("PYKConsoleQuickLookController").new()
pyk.setCurrentItems=ns(j.items)
pvc=QLPreviewController.new()
pvc.dataSource=j.objcinstance
import ui
v=ui.View(frame=(0,0,400,400))
v.content_mode=ui.CONTENT_SCALE_ASPECT_FIT
ObjCInstance(v).addSubview_(pvc.view())
pvc.view.frame=ObjCInstance(v).bounds
v.present('sheet')
'''

def ObjCBlockWrapper(argtypes=c_void_p, restype=None):
   def deco(func):
      def wrapper(*args,**kwargs):
         return func(*args,**kwargs)
      def blk(*args,**kwargs):
          ObjCBlock(wrapper,restype,argtypes).__call__
      #return wrapper
   return deco
   

