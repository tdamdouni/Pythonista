# https://forum.omz-software.com/topic/4508/phone-vibrator

# It’s possible, though it requires using private APIs (might break in future iOS updates etc.). Here’s an example, adapted from this StackOverflow answer:

from objc_util import *
from ctypes import c_ulong

def vibrate_pattern(on_off_times):
    pattern = ns([])
    for i, t in enumerate(on_off_times):
        on = NSNumber.numberWithBool_(i % 2 == 0)
        pattern.addObject_(on)
        pattern.addObject_(t)
    c.AudioServicesPlaySystemSoundWithVibration.argtypes = [c_ulong, c_void_p, c_void_p]
    c.AudioServicesPlaySystemSoundWithVibration.restype = None
    vibe_info = ns({'VibePattern': pattern, 'Intensity': 1.0})
    c.AudioServicesPlaySystemSoundWithVibration(4095, None, vibe_info.ptr)

if __name__ == '__main__':
    vibrate_pattern([200, 50, 200, 50, 200, 50, 800])

# The on_off_times parameter should be a list of numbers, specifying a sequence of “vibrate” and “pause” durations in milliseconds.
