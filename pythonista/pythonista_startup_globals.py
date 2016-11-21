# coding: utf-8

# https://forum.omz-software.com/topic/2175/you-can-t-take-my-globals-from-me

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

# why & how to use pythonista_startup.py sub-module to keep *globals*

# Every time you run a script, Pythonista deletes all global variables, except for those that come from the pythonista_startup module (which is run automatically when the app is started). Internally this is done by looking at dir(pythonista_startup) - any names listed there are not deleted from the globals. I'm abusing this feature just a tiny bit so that no globals are ever removed.

# The first class, ContainAllTheThings, is a subclass of list that pretends to contain every object, i. e. obj in ContainAllTheThings() is always True for any object. The second class, DirAllTheThings, is a subclass of module (aka types.ModuleType) with a modified __dir__ method that returns a ContainAllTheThings object. This means that obj in dir(DirAllTheThings()) is always True. Finally we replace the real module pythonista_startup with a DirAllTheThings object and copy all attributes over.

# To find out which global names come from pythonista_startup, Pythonista internally checks name in dir(pythonista_startup) for every name. Now we've replaced pythonista_startup with an instance of DirAllTheThings, meaning that when we call dir on it we get an instance of ContainAllTheThings. Now when Pythonista checks whether a name comes from pythonista_startup, the answer is always True, meaning that no name is ever deleted.

