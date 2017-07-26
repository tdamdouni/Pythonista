# https://gist.github.com/pudquick/581a71425439f2cf8f09

# https://forum.omz-software.com/topic/3125/calling-into-sysctl

from ctypes import CDLL, c_uint, byref, create_string_buffer
from ctypes.util import find_library
libc = CDLL(find_library("c"))

def sysctl(name, isString=True):
    size = c_uint(0)
    # Find out how big our buffer will be
    libc.sysctlbyname(name, None, byref(size), None, 0)
    # Make the buffer
    buf = create_string_buffer(size.value)
    # Re-run, but provide the buffer
    libc.sysctlbyname(name, buf, byref(size), None, 0)
    if isString:
        return buf.value
    else:
        return buf.raw
