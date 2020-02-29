# coding: utf-8

# https://forum.omz-software.com/topic/2493/ui-control-subclassing-really-good-idea

'''
dict of  dicts
 key == x.__class.__name__
 value = dict of the defaults for the object
'''
from __future__ import print_function
_std_defaults = \
    {
        'Button' : {
                            'tint_color': 'black',
                            'width' : 80,
                            'height' : 32,
                            'background_color' : 'yellow',
                            'x' : 100,
                            'y' : 200,
                            },
    }

class ControlExt(ui.View):
    def __init__(self , ui_object, *args, **kwargs):
        print('in here, ControlExt init')
        print(kwargs)
        self.obj = ui_object()
        
        self.std_object_creation(self.obj)  
        self.set_obj_args(self.obj, *args, **kwargs)
        
    def __setattr__(self, name,value):
        if name not in ['frame','width','height','x','y','flex','hidden','transform']:
            if hasattr(self,'obj'):
                if name in dir(self.obj):
                    object.__setattr__(self.obj,name,value)

        object.__setattr__(self,name,value)
        
    def __getattribute__(self,name):
        try:
            return object.__getattribute__(self,name)
        except AttributeError:
            if hasattr(self,'obj') and name in dir(self.obj):
                return object.__getattribute__(self.obj,name)
            else:
                raise
                    
    # dont use the obj init to set the args, kwargs
    def set_obj_args(obj, *args, **kwargs):
        print('set_obj_args args etc', kwargs)
        for k,v in kwargs.iteritems():
            if hasattr(obj, k):
                if k == 'image':
                    setattr(obj, k , self.get_named_ui_image(v))
                else:
                    setattr(obj, k, v)
        
    def get_named_ui_image(self, image_name):
        return ui.Image.named(image_name)
    
    def std_object_creation(self, obj):
        #set the attrs of the object as created without passing attrs
        class_str = obj.__class__.__name__
        obj_defaults = _std_defaults.get(class_str, False)
        if not obj_defaults: return
        
        print('in here, std_object_creation', obj_defaults)
        for k,v in obj_defaults.iteritems():
            if hasattr(obj, k):
                if k == 'image':
                    setattr(obj, k , self.get_named_ui_image(v))
                else:
                    print('std_object_creation', k, v)
                    setattr(obj, k, v)

# we need to create one per ui. class type  
class _uiButtonExt(ControlExt):
    '''
        Can do ui.Button specfic stuff here
    '''
    def __init__(self, *args, **kwargs):
        ControlExt.__init__(self, ui.Button, *args, **kwargs)
        

# we only want to deal with this class      
class uiButtonExt(_uiButtonExt):
    def __init__(self, *args, **kwargs):
        _uiButtonExt.__init__(self, *args, **kwargs)
    
    
        
if __name__ == '__main__':
    f = (0,0, 500, 500)
    
    v = ui.View(frame = f )
    v.present('sheet')
    

    btn = uiButtonExt(width = 300, heigth = 32,  title = 'tom jones', tint_color = 'orange', bg_color = 'black')
    
    v.add_subview(btn)
    