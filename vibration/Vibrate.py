# coding: utf-8

# https://forum.omz-software.com/topic/2093/vibrate-module

import ctypes
import time
c = ctypes.CDLL(None)

def vibrate():
    p = c.AudioServicesPlaySystemSound
    p.restype, p.argtypes = None, [ctypes.c_int32]
    vibrate_id = 0x00000fff
    p(vibrate_id)

if __name__ == '__main__':
    for i in xrange(3):
        vibrate()
        time.sleep(0.5)