# coding: utf-8

# https://forum.omz-software.com/topic/2876/pydia-a-package-installer-for-pythonista/2

 from objc_util import *

c= ObjCClass.get_names(prefix='UI')+ObjCClass.get_names(prefix='NS')
for cls in c:
	if not cls.startswith('_'):
		try:
			globals()[cls]=ObjCClass(cls)
		except ValueError:
			pass
			
#==============================

from objc_util import ObjCClass
globals().update({n: ObjCClass(n) for n in ObjCClass.get_names('UI')})

