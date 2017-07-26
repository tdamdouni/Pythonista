# https://forum.omz-software.com/topic/3288/ctypes-pythonapi-version/2

import ctypes

p3 = ctypes.pythonapi
state = p3.PyGILState_Ensure()
p3.PyRun_SimpleString('print(42)')
p3.PyGILState_Release(state)
