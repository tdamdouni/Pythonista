# https://forum.omz-software.com/topic/3905/wifi-ssid/7

# @omz

from objc_util import *

def get_ssid():
	CNCopyCurrentNetworkInfo = c.CNCopyCurrentNetworkInfo
	CNCopyCurrentNetworkInfo.restype = c_void_p
	CNCopyCurrentNetworkInfo.argtypes = [c_void_p]
	info = ObjCInstance(CNCopyCurrentNetworkInfo(ns('en0')))
	return str(info['SSID'])
	
print('Current SSID:', get_ssid())

