# coding: utf-8
# determine the version of Pythonista
# https://github.com/Phuket2/Pythonista/blob/master/ideas/pythonistia_version
from __future__ import print_function
try:
	__import__('imp').find_module('dialogs')
	__PISTA_VER__ = 1.6
except ImportError:
	__PISTA_VER__ = 1.5
	
# coding: utf-8
import timeit


def PythonistaVersion():
	try:
		__import__('imp').find_module('dialogs')
		return 1.6
	except ImportError:
		return 1.5
		
def PythonistaVersion2():
	try:
		import dialogs
		return 1.6
	except ImportError:
		return 1.5
		
		
		
print(timeit.Timer('PythonistaVersion',setup="from __main__ import PythonistaVersion").timeit())

print(timeit.Timer('PythonistaVersion2',setup="from __main__ import PythonistaVersion2").timeit())

