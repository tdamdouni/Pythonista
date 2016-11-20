# coding: utf-8

# https://forum.omz-software.com/topic/2444/determining-pythonista-s-version/10

# You could also check all available Python versions at once. The different PythonistaKit frameworks can be accessed using ctypes, so you can do something like this:

import ctypes
import os
import sys

FRAMEWORKS = os.path.join(os.path.dirname(sys.executable), "Frameworks")

def get_python_version(name):
	dll = ctypes.CDLL(os.path.join(FRAMEWORKS, name + ".framework", name))
	dll.Py_GetVersion.argtypes = []
	dll.Py_GetVersion.restype = ctypes.c_char_p
	return dll.Py_GetVersion().decode("ascii")
	
print(get_python_version('PythonistaKit'))
print(get_python_version('PythonistaKit3'))

