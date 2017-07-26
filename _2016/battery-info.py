# https://pythonista-app.slack.com/archives/codinghelp/p1486525124001364

from objc_util import *
from ctypes import *
c.IOServiceMatching.argtypes=[c_char_p]
kIOMasterPortDefault=c_int32.in_dll(c,'kIOMasterPortDefault')
srv=ObjCInstance(c.IOServiceMatching(b"IOPMPowerSource"))
c.IOServiceGetMatchingService.argtypes=[c_long,c_void_p]
powerSource = c.IOServiceGetMatchingService(kIOMasterPortDefault, srv);
#c.IOServiceGetMatchingService
c.IORegistryEntryCreateCFProperties.argtypes=[c_int32,c_void_p, c_void_p, c_int32 ]

batteryProperties=c_void_p(0)

c.IORegistryEntryCreateCFProperties(powerSource, byref(batteryProperties), None, 0);

print(ObjCInstance(batteryProperties))
