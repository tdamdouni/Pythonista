# https://gist.github.com/jsbain/e18bb2039eda061ee7a7d7034b358aa0

# https://forum.omz-software.com/topic/3891/is-it-possible-to-use-quicklook-in-an-ui-view/6

from objc_util import *
import weakref

QLPreviewController=ObjCClass("QLPreviewController")

def objcmethod(fcn):
	'''wrap fcn(self,_self,_sel,...) in a staticmethod subtracting first arg
		fcn(self,sel,args...)
	'''
	fcn._objcmethod=True
	return staticmethod(fcn)
def get_objc_methods(cls):
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
		cls.instances[self.objcinstance.ptr]=weakref.ref(self)
	def get_instance(*args):
		if args:
			return cls.instances[args[0]]()
		else:
			return cls()

	cls.__init__=__init__

	return get_instance

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

pvc=QLPreviewController.new()
pvc.dataSource=j.objcinstance
import ui
v=ui.View(frame=(0,0,400,400))
v.content_mode=ui.CONTENT_SCALE_ASPECT_FIT
ObjCInstance(v).addSubview_(pvc.view())
pvc.view.frame=ObjCInstance(v).bounds
v.present('sheet')
