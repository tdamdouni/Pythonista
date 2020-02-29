from __future__ import print_function
# https://forum.omz-software.com/topic/1951/getting-the-battery-level-and-battery-state-of-the-device/10

from objc_util import *
device = ObjCClass('UIDevice').currentDevice()
device.setBatteryMonitoringEnabled_(True)
print('Battery level:', device.batteryLevel())
device.setBatteryMonitoringEnabled_(False)
