# coding: utf-8

# https://forum.omz-software.com/topic/2175/you-can-t-take-my-globals-from-me/4

from __future__ import division, print_function

import sys
import types

class ContainAllTheThings(list):
    def __getitem__(self, key):
        try:
            return super(ContainAllTheThings, self).__getitem__(key)
        except (IndexError, KeyError):
            return None
    
    def __contains__(self, obj):
        return super(ContainAllTheThings, self).__contains__(obj) or True

class DirAllTheThings(types.ModuleType):
    def __dir__(self):
        return ContainAllTheThings()

new_module = DirAllTheThings(__name__, __doc__)
vars(new_module).update(vars(sys.modules["pythonista_startup"]))
sys.modules["pythonista_startup"] = new_module

# --------------------

# python3 version

import sys
import types

class DirAllTheGlobals(types.ModuleType):
    import __main__
    
    def __dir__(self):
        return dir(type(self).__main__)

# THESE LINES MUST COME LAST.
# Anything past this point is executed in the context of the old
# pythonista_startup module, which may already be partially
# garbage-collected.
new_module = DirAllTheGlobals(__name__, __doc__)
vars(new_module).update(vars(sys.modules["pythonista_startup"]))
sys.modules["pythonista_startup"] = new_module

# --------------------
