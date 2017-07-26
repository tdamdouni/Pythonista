# coding: utf-8

# https://forum.omz-software.com/topic/2513/getting-the-parent-of-a-dynamically-method-as-a-function/46

import types

class Extender(object):
    def __new__(cls, target_instance, *args, **kwargs):
        if isinstance(cls.__init__, types.MethodType):
            cls.__init__.__func__(target_instance, *args, **kwargs)
        extender_instance = super(Extender, cls).__new__(cls)
        for key in dir(extender_instance):
            if key.startswith('__'): continue
            value = getattr(extender_instance, key)
            if callable(value):
                setattr(target_instance, key, types.MethodType(value.__func__, target_instance))
            else:
                setattr(target_instance, key, value)
        return target_instance

# fixed a bug self.methods can be called in __init__

import types

class Extender(object):
    def __new__(extender_subclass, target_instance, *args, **kwargs):
        extender_instance = super(Extender, extender_subclass).__new__(extender_subclass)
        for key in dir(extender_instance):
            if key.startswith('__'): continue
            value = getattr(extender_instance, key)
            if callable(value):
                setattr(target_instance, key, types.MethodType(value.__func__, target_instance))
            else:
                setattr(target_instance, key, value)
        if isinstance(extender_subclass.__init__, types.MethodType):
            extender_subclass.__init__.__func__(target_instance, *args, **kwargs)
        return target_instance
        
