# coding: utf-8

# @dgelssus

# https://forum.omz-software.com/topic/2447/hackathon-challenge-set-by-ccc-started-new-thread/8

# https://github.com/dgelessus/pythonista-scripts/blob/master/moduledump.py

import collections
import inspect
import importlib
import io
import os
import sys
import types

def flatten(seq):
    for obj in seq:
        try:
            it = iter(obj)
        except TypeError:
            yield obj
        else:
            for o in flatten(obj):
                yield o

def sorted_mapping(mapping, **kwargs):
    out = collections.OrderedDict()
    
    for k in sorted(mapping.keys(), **kwargs):
        out[k] = mapping[k]
    
    return out

def order_classes(classes):
    classes = list(classes)
    ordered = list(flatten(inspect.getclasstree(classes)))
    
    ordered.reverse()
    
    for cls in list(ordered):
        if cls not in classes or ordered.count(cls) > 1:
            ordered.remove(cls)
    
    ordered.reverse()
    
    return ordered

def order_attributes(attrs):
    constants = {}
    functions = {}
    classes = {}
    
    for key, value in attrs.items():
        if isinstance(value, type(int.real)) or key in ("__abstractmethods__", "__base__", "__bases__", "__class__", "__dict__", "__dictoffset__", "__file__", "__flags__", "__itemsize__", "__module__", "__name__", "__package__", "__subclasses__", "__weakrefoffset__"):
            pass
        elif isinstance(value, (type, types.ClassType)):
            classes[key] = value
        elif isinstance(value, (types.FunctionType, types.BuiltinFunctionType, type(list.append), type(object.__init__), classmethod, staticmethod)):
            if not (key.startswith("__") and key.endswith("__")):
                functions[key] = value
        else:
            constants[key] = value
    
    constants = sorted_mapping(constants)
    functions = sorted_mapping(functions)
    classes = sorted_mapping(classes)
    classes_reverse = collections.OrderedDict((v, k) for k, v in classes.items())
    
    classes_ordered = collections.OrderedDict((classes_reverse[cls], cls) for cls in order_classes(classes.values()))
    
    return collections.OrderedDict(constants.items() + functions.items() + classes_ordered.items())

def stringify_constant(name, value):
    return u"{} = {!r}".format(name, value)

def stringify_function(name, value):
    return u"def {}(*args, **kwargs): pass".format(name)

def stringify_classmethod(name, value):
    return u"def {}(cls, *args, **kwargs): pass".format(name)

def stringify_method(name, value):
    return u"def {}(self, *args, **kwargs): pass".format(name)

def stringify_class(name, value):
    attrs = list((k, v) for k, v in inspect.getmembers(value) if not hasattr(super(value), k) or v != getattr(super(value), k))
    
    if type(value) not in [type(cls) for cls in value.__bases__]:
        attrs = [("__metaclass__", type(value))] + attrs
    
    body = u"\n".join(u"    " + line for line in stringify_attributes(order_attributes(collections.OrderedDict(attrs))).splitlines())
    
    return u"\nclass {}({}):\n{}".format(name, ", ".join(cls.__name__ for cls in value.__bases__), body)

def stringify_attributes(attrs):
    lines = []
    
    for k, v in attrs.items():
        if isinstance(v, (type, types.ClassType)):
            lines.append(stringify_class(k, v))
        elif isinstance(v, (types.MethodType, type(list.append), type(object.__init__))):
            lines.append(stringify_method(k, v))
        elif isinstance(v, classmethod):
            lines.append(stringify_classmethod(k, v))
        elif isinstance(v, (types.FunctionType, types.BuiltinFunctionType, staticmethod)):
            lines.append(stringify_function(k, v))
        else:
            lines.append(stringify_constant(k, v))
    
    return u"\n".join(lines)

if __name__ == "__main__":
    name = sys.argv[1]
    
    with io.open(os.extsep.join((name, u"py")), "w") as f:
        f.write(stringify_attributes(order_attributes(collections.OrderedDict(inspect.getmembers(importlib.import_module(name))))))