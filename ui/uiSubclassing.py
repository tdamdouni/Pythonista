# coding: utf-8

# https://gist.github.com/Phuket2/f337b7d82d1c3fd77a68

# https://forum.omz-software.com/topic/2493/ui-control-subclassing-really-good-idea/9

from __future__ import print_function
import ui 
'''
dict of  dicts
 key == x.__class.__name__
 value = dict of the defaults for the object
'''
_std_defaults = \
	{
		'Button' : {
							'tint_color': 'blue',
							'width' : 80,
							'height' : 32,
							'background_color' : None,
							'x' : 0,
							'y' : 0,
							'title' : 'fred',
							'border_width' : .5,
							'corner_radius' : 3,
							'name' : 'ButtonTest',
						},
	}
	
_attr_ignore_attrs = \
	{
		'Button'	: \
			['frame','width','height','x','y','flex',
				'hidden','transform', 'border_width, corner_radius, background_color'],
				
	}

class ControlExt(ui.View):
	def __init__(self , ui_object, *args, **kwargs):
		self.obj = ui_object()
		self.hidden = True
		self.add_subview(self.obj)
		self.obj.flex = 'WH'
		
		
		
		if kwargs.get('parent', False):
			print('we have a parent')
			if kwargs.get('add', False):
				print('we will add ourself to parent')
				kwargs.get('parent').add_subview(self)
	
		#self.ignore_attr_list = object.get_attr_ignore_list()
		
		self.std_object_creation(self.obj)	
		self.set_obj_args(self.obj, *args, **kwargs)
		
		
		
	def __setattr__(self, name,value):
		# flex, frame taken out
		if name not in ['width','height','x','y','hidden','transform'
		 'border_width, corner_radius, background_color']:
			if hasattr(self,'obj'):
				if name in dir(self.obj):
					print(name, value)
					object.__setattr__(self.obj,name,value)
				
		object.__setattr__(self,name,value)
		
		f = self.frame # limit the calls to set/get scary...
		# i cant get flex to work... doing it with a hammer for now
		object.__setattr__(self.obj, 'frame', (0,0,f[2], f[3]))
		
		
	def __getattribute__(self,name):
		try:
			return object.__getattribute__(self,name)
		except AttributeError:
		
			if hasattr(self,'obj') and name in dir(self.obj):
				return object.__getattribute__(self.obj,name)
			else:
				raise
					
	# dont use the obj init to set the args, kwargs
	def set_obj_args(self , obj, *args, **kwargs):
		for k,v in kwargs.iteritems():
			if hasattr(obj, k):
				if k == 'image':
					setattr(obj, k , self.get_named_ui_image(v))
				else:
					setattr(obj, k, v)
				print('**object kwargs ', k,v)
		
	def get_named_ui_image(self, image_name):
		return ui.Image.named(image_name)
	
	def std_object_creation(self, obj):
		#set the attrs of the object as created without passing attrs
		class_str = obj.__class__.__name__
		obj_defaults = _std_defaults.get(class_str, False)
		if not obj_defaults: return
		
		for k, v in obj_defaults.iteritems():
			if hasattr(obj, k):
				if k == 'image':
					setattr(obj, k , self.get_named_ui_image(v))
				else:
					setattr(obj, k, v)
				print('**creation ', k,v)
				
	def get_attr_ignore_list(self):
		return  _attr_ignore_attrs.get(self.obj.__class__.__name__, [])
			
	#def layout(self):
		#self.obj.frame = self.frame
		
	def how_did_we_get_here(self):
		object.__setattr__(self.obj, 'frame', (0,0,f[2], f[3]))
		

# we need to create one per ui. class type	
class _uiButtonExt(ControlExt):
	'''
		Can do ui.Button specfic stuff here
	'''
	def __init__(self, *args, **kwargs):
		# support adding to subview
		
		ControlExt.__init__(self, ui.Button, *args, **kwargs)
		# LOL, do it before the call to the super or not...
		# i have tried both ways. i am sure i will learn the hard way
		'''
		if kwargs.get('parent', False):
			print 'we have a parent'
			if kwargs.get('add', False):
				print 'we will add ourself to parent'
				kwargs.get('parent').add_subview(self)
		'''
		self.hidden = False
		
		
	# would be nice to offer some positional func..
	def please_center(self):
		self.center = (self.superview.bounds.center())
	
	def pos_br(self):
		l,t,h,w = self.superview.bounds
		ow, oh = self.obj.frame[2],self.obj.frame[3]
		self.frame = (w - ow, h - oh, h, w)
		#self.how_did_we_get_here()
		#f1 = ()
		
# we only want to deal with this class		
class uiButtonExt(_uiButtonExt ):
	def __init__(self, *args, **kwargs):
		_uiButtonExt.__init__(self, *args, **kwargs)
		
	
	
	
def btn_action(sender):
	print('btn hit')
	
if __name__ == '__main__':
	f = (0,0, 500, 500)
	
	v = ui.View(frame = f )
	#v.hidden = True
	v.present('sheet')
	
	btn = uiButtonExt(parent = v, add = True, bg_color = 'purple', tint_color = 'white', action = btn_action, width = 50, height = 32)
	btn.please_center()
	
	#btn.pos_br()
	#v.hidden = False