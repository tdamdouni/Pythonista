# coding: utf-8

# python3

# https://forum.omz-software.com/topic/2175/you-can-t-take-my-globals-from-me/4

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

