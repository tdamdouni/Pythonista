from objc_util import *

UIDevice = ObjCClass('UIDevice')
device = UIDevice.currentDevice()
battery_states = {1: 'unplugged', 2:'charging', 3: 'full'}

device.setBatteryMonitoringEnabled_(True)
battery_percent = device.batteryLevel() * 100
state = device.batteryState()
state_str = battery_states.get(state,'unknown')
print('Battery Level: %0.1f%% (%s)' %(battery_percent, state_str))
device.setBatteryMonitoringEnabled_(False)
