# coding: utf-8

# Captured from: _https://forum.omz-software.com/topic/1951/getting-the-battery-level-and-battery-state-of-the-device_

def get_battery_level():
   '''[[UIDevice currentDevice] setBatteryMonitoringEnabled:YES]]
   [[UIDevice currentDevice] batteryLevel];
   [[UIDevice currentDevice] batteryState];
   '''
   UIDevice = cls('UIDevice')    
   currentDevice = msg(UIDevice, c_void_p, 'currentDevice')
   msg(currentDevice,None,'setBatteryMonitoringEnabled:',[c_bool],True)
   b=msg(currentDevice,c_float,'batteryLevel')
   return b

###==============================

# coding: utf-8

from ctypes import cdll, c_void_p, c_char_p, c_int, c_bool, c_float
c = cdll.LoadLibrary(None)

def get_current_device():
    c.sel_registerName.restype = c_void_p
    c.sel_registerName.argtypes = [c_char_p]
    c.objc_getClass.restype = c_void_p
    c.objc_getClass.argtypes = [c_char_p]
    UIDevice = c.objc_getClass('UIDevice')
    c.objc_msgSend.argtypes = [c_void_p, c_void_p]
    c.objc_msgSend.restype = c_void_p
    device = c.objc_msgSend(UIDevice, c.sel_registerName('currentDevice'))
    return device

def set_battery_monitoring_enabled(flag):
    device = get_current_device()
    c.objc_msgSend.argtypes = [c_void_p, c_void_p, c_bool]
    c.objc_msgSend.restype = None
    c.objc_msgSend(device, c.sel_registerName('setBatteryMonitoringEnabled:'), c_bool(flag))

def get_battery_level():
    device = get_current_device()
    c.objc_msgSend.argtypes = [c_void_p, c_void_p]
    c.objc_msgSend.restype = c_float
    battery_level = c.objc_msgSend(device, c.sel_registerName('batteryLevel'))
    return battery_level

def get_battery_state():
    device = get_current_device()
    c.objc_msgSend.argtypes = [c_void_p, c_void_p]
    c.objc_msgSend.restype = c_int
    battery_state = c.objc_msgSend(device, c.sel_registerName('batteryState'))
    return battery_state

def main():
    set_battery_monitoring_enabled(True)
    battery_level = get_battery_level()
    print 'Battery Level: %0.1f<p>&#8217; % (battery_level * 100.0,)
 battery_state = get_battery_state()
 states = {0: &#8216;unknown&#8217;, 1: &#8216;unplugged&#8217;, 2: &#8216;charging&#8217;, 3: &#8216;full&#8217;}
 print &#8216;Battery State: %i (%s)&#8217; % (battery_state, states.get(battery_state))
 set_battery_monitoring_enabled(False)</p>

<p>if <strong>name</strong> == &#8216;<strong>main</strong>&#8217;:
 main()</p>

<h1>==============================</h1>

<p>import contextlib</p>

<p>@contextlib.contextmanager
def battery_monitoring_enabled():
 set_battery_monitoring_enabled(True)
 yield
 set_battery_monitoring_enabled(False)</p>

<h1>==============================</h1>

<p>def main():
 with battery_monitoring_enabled():
 battery_level = get_battery_level()
 print &#8217;Battery Level: %0.1f</p>' % (battery_level * 100.0,)
        battery_state = get_battery_state()
        states = {0: 'unknown', 1: 'unplugged', 2: 'charging', 3: 'full'}
        print 'Battery State: %i (%s)' % (battery_state, states.get(battery_state))

###==============================

# coding: utf-8

#See: http://omz-forums.appspot.com/pythonista/post/5776493279969280

import contextlib
from ctypes import cdll, c_void_p, c_char_p, c_int, c_bool, c_float
c = cdll.LoadLibrary(None)

objc_types = cdll, c_void_p, c_char_p, c_int, c_bool, c_float
return_types = list(objc_types) + [None]

def objc_call(return_type, obj, sel_name, *args):
    assert return_type in return_types, '{} is an invalid return type.'.format(return_type)
    assert isinstance(sel_name, basestring), '{} is an invalid sel_name.'.format(sel_name)
    arg_types = [c_void_p, c_void_p]
    if args:
        fmt = 'arg[{}] has an invalid arg_type: {}.'
        for i, arg in enumerate(args):
            arg_type = type(arg)
            assert arg_type in objc_types, fmt.format(i, arg_type)
            arg_types.append(arg_type)
    c.objc_msgSend.argtypes = arg_types
    c.objc_msgSend.restype = return_type
    return c.objc_msgSend(obj, c.sel_registerName(sel_name), *args)

def get_current_device():
    c.sel_registerName.restype = c_void_p
    c.sel_registerName.argtypes = [c_char_p]
    c.objc_getClass.restype = c_void_p
    c.objc_getClass.argtypes = [c_char_p]
    UIDevice = c.objc_getClass('UIDevice')
    return objc_call(c_void_p, UIDevice, 'currentDevice')

def set_battery_monitoring_enabled(flag):
    objc_call(None, get_current_device(), 'setBatteryMonitoringEnabled:', c_bool(flag))

import contextlib
@contextlib.contextmanager
def battery_monitoring_enabled():
    set_battery_monitoring_enabled(True)
    yield
    set_battery_monitoring_enabled(False)

def get_battery_level():
    return objc_call(c_float, get_current_device(), 'batteryLevel')

def get_battery_state():
    return objc_call(c_int, get_current_device(), 'batteryState')

def main():
    with battery_monitoring_enabled():
        battery_level = get_battery_level()
        print 'Battery Level: %0.1f%%' % (battery_level * 100.0,)
        battery_state = get_battery_state()
        states = {0: 'unknown', 1: 'unplugged', 2: 'charging', 3: 'full'}
        print 'Battery State: %i (%s)' % (battery_state, states.get(battery_state))

if __name__ == '__main__':
    main()

###==============================

import contextlib

@contextlib.contextmanager
def battery_monitoring_enabled():
    set_battery_monitoring_enabled(True)
    try:
        yield
    finally:
        set_battery_monitoring_enabled(False)

###==============================

from objc_util import *
device = ObjCClass('UIDevice').currentDevice()
device.setBatteryMonitoringEnabled_(True)
print 'Battery level:', device.batteryLevel()
device.setBatteryMonitoringEnabled_(False)
ctype# --------------------
def get_battery_level():
   '''[[UIDevice currentDevice] setBatteryMonitoringEnabled:YES]]
   [[UIDevice currentDevice] batteryLevel];
   [[UIDevice currentDevice] batteryState];
   '''
   UIDevice = cls('UIDevice')    
   currentDevice = msg(UIDevice, c_void_p, 'currentDevice')
   msg(currentDevice,None,'setBatteryMonitoringEnabled:',[c_bool],True)
   b=msg(currentDevice,c_float,'batteryLevel')
   return b
# --------------------
# coding: utf-8
from ctypes import cdll, c_void_p, c_char_p, c_int, c_bool, c_float
c = cdll.LoadLibrary(None)

def get_current_device():
    c.sel_registerName.restype = c_void_p
    c.sel_registerName.argtypes = [c_char_p]
    c.objc_getClass.restype = c_void_p
    c.objc_getClass.argtypes = [c_char_p]
    UIDevice = c.objc_getClass('UIDevice')
    c.objc_msgSend.argtypes = [c_void_p, c_void_p]
    c.objc_msgSend.restype = c_void_p
    device = c.objc_msgSend(UIDevice, c.sel_registerName('currentDevice'))
    return device

def set_battery_monitoring_enabled(flag):
    device = get_current_device()
    c.objc_msgSend.argtypes = [c_void_p, c_void_p, c_bool]
    c.objc_msgSend.restype = None
    c.objc_msgSend(device, c.sel_registerName('setBatteryMonitoringEnabled:'), c_bool(flag))

def get_battery_level():
    device = get_current_device()
    c.objc_msgSend.argtypes = [c_void_p, c_void_p]
    c.objc_msgSend.restype = c_float
    battery_level = c.objc_msgSend(device, c.sel_registerName('batteryLevel'))
    return battery_level

def get_battery_state():
    device = get_current_device()
    c.objc_msgSend.argtypes = [c_void_p, c_void_p]
    c.objc_msgSend.restype = c_int
    battery_state = c.objc_msgSend(device, c.sel_registerName('batteryState'))
    return battery_state

def main():
    set_battery_monitoring_enabled(True)
    battery_level = get_battery_level()
    print 'Battery Level: %0.1f%%' % (battery_level * 100.0,)
    battery_state = get_battery_state()
    states = {0: 'unknown', 1: 'unplugged', 2: 'charging', 3: 'full'}
    print 'Battery State: %i (%s)' % (battery_state, states.get(battery_state))
    set_battery_monitoring_enabled(False)

if __name__ == '__main__':
    main()
# --------------------
ctype# --------------------
import contextlib

@contextlib.contextmanager
def battery_monitoring_enabled():
    set_battery_monitoring_enabled(True)
    yield
    set_battery_monitoring_enabled(False)
# --------------------
main()# --------------------
with# --------------------
def main():
    with battery_monitoring_enabled():
        battery_level = get_battery_level()
        print 'Battery Level: %0.1f%%' % (battery_level * 100.0,)
        battery_state = get_battery_state()
        states = {0: 'unknown', 1: 'unplugged', 2: 'charging', 3: 'full'}
        print 'Battery State: %i (%s)' % (battery_state, states.get(battery_state))
# --------------------
with# --------------------
set_battery_monitoring_enabled(False)# --------------------
with# --------------------
objc_call(return_type, obj, sel_name, *args)# --------------------
get_current_device()# --------------------
get_battery_level()# --------------------
get_battery_state()# --------------------
set_battery_monitoring_enabled()# --------------------
:# --------------------
set_battery_monitoring_enabled()# --------------------
# coding: utf-8

#See: http://omz-forums.appspot.com/pythonista/post/5776493279969280

import contextlib
from ctypes import cdll, c_void_p, c_char_p, c_int, c_bool, c_float
c = cdll.LoadLibrary(None)

objc_types = cdll, c_void_p, c_char_p, c_int, c_bool, c_float
return_types = list(objc_types) + [None]

def objc_call(return_type, obj, sel_name, *args):
    assert return_type in return_types, '{} is an invalid return type.'.format(return_type)
    assert isinstance(sel_name, basestring), '{} is an invalid sel_name.'.format(sel_name)
    arg_types = [c_void_p, c_void_p]
    if args:
        fmt = 'arg[{}] has an invalid arg_type: {}.'
        for i, arg in enumerate(args):
            arg_type = type(arg)
            assert arg_type in objc_types, fmt.format(i, arg_type)
            arg_types.append(arg_type)
    c.objc_msgSend.argtypes = arg_types
    c.objc_msgSend.restype = return_type
    return c.objc_msgSend(obj, c.sel_registerName(sel_name), *args)

def get_current_device():
    c.sel_registerName.restype = c_void_p
    c.sel_registerName.argtypes = [c_char_p]
    c.objc_getClass.restype = c_void_p
    c.objc_getClass.argtypes = [c_char_p]
    UIDevice = c.objc_getClass('UIDevice')
    return objc_call(c_void_p, UIDevice, 'currentDevice')

def set_battery_monitoring_enabled(flag):
    objc_call(None, get_current_device(), 'setBatteryMonitoringEnabled:', c_bool(flag))

import contextlib
@contextlib.contextmanager
def battery_monitoring_enabled():
    set_battery_monitoring_enabled(True)
    yield
    set_battery_monitoring_enabled(False)

def get_battery_level():
    return objc_call(c_float, get_current_device(), 'batteryLevel')

def get_battery_state():
    return objc_call(c_int, get_current_device(), 'batteryState')

def main():
    with battery_monitoring_enabled():
        battery_level = get_battery_level()
        print 'Battery Level: %0.1f%%' % (battery_level * 100.0,)
        battery_state = get_battery_state()
        states = {0: 'unknown', 1: 'unplugged', 2: 'charging', 3: 'full'}
        print 'Battery State: %i (%s)' % (battery_state, states.get(battery_state))

if __name__ == '__main__':
    main()
# --------------------
'setBatteryMonitoringEnabled:'# --------------------
import contextlib

@contextlib.contextmanager
def battery_monitoring_enabled():
    set_battery_monitoring_enabled(True)
    try:
        yield
    finally:
        set_battery_monitoring_enabled(False)
# --------------------
from objc_util import *
device = ObjCClass('UIDevice').currentDevice()
device.setBatteryMonitoringEnabled_(True)
print 'Battery level:', device.batteryLevel()
device.setBatteryMonitoringEnabled_(False)

# --------------------
