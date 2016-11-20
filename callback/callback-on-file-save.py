objc_util# --------------------
old_print = print

def print(*args, **kwargs):
    old_print("Hi!", *args, **kwargs)
# --------------------
print# --------------------
print# --------------------
old_print# --------------------
def _make_new_print():
    old_print = print
    def new_print(*args, **kwargs):
        old_print("Hi!", *args, **kwargs)
    return new_print

print = _make_new_print()
del _make_new_print
# --------------------
# coding: utf-8
# coding: utf-8
import editor
from objc_util import *
from objc_util import parse_types
import ctypes
import inspect
t=editor._get_editor_tab()

def saveData(_self,_sel):
    print 'hi'  
    #call original method
    obj=ObjCInstance(_self)
    orig=getattr(obj,'_original'+c.sel_getName(_sel))
    orig()

def swizzle(cls, old_sel, new_fcn):
    '''swizzles cls.old_sel with new_fcn.  Assumes encoding is the same.
    if class already has swizzledSelector, unswizzle first.
    original selector can be called via originalSelectir
    
    '''
    orig_method=c.class_getInstanceMethod(cls.ptr, sel(old_sel))
    #new_method=c.class_getInstanceMethod(cls, sel(new_sel))
    type_encoding=str(cls.instanceMethodSignatureForSelector_(sel(old_sel))._typeString())
    parsed_types = parse_types(str(type_encoding))
    restype = parsed_types[0]
    argtypes = parsed_types[1]
    # Check if the number of arguments derived from the selector matches the actual function:
    argspec = inspect.getargspec(new_fcn)
    if len(argspec.args) != len(argtypes):
        raise ValueError('%s has %i arguments (expected %i)' % (method, len(argspec.args), len(argtypes)))
    IMPTYPE = ctypes.CFUNCTYPE(restype, *argtypes)
    imp = IMPTYPE(new_fcn)
    retain_global(imp)
    new_sel='_original'+old_sel
    didAdd=c.class_addMethod(cls.ptr, sel(new_sel), imp, type_encoding)
    new_method=c.class_getInstanceMethod(cls.ptr, sel(new_sel))
    # swap imps
    c.method_exchangeImplementations.restype=None
    c.method_exchangeImplementations.argtypes=[c_void_p,c_void_p]
    c.method_exchangeImplementations(orig_method, new_method)
    return new_sel


t=editor._get_editor_tab()

cls=ObjCInstance(c.object_getClass(t.ptr))
swizzle(cls,'saveData',saveData)

                                            
                                            
# --------------------
