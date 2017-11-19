from objc_util import  *
load_framework('SystemConfiguration')
c.CNCopySupportedInterfaces.argtypes=[]
c.CNCopySupportedInterfaces.restype=c_void_p
c.CNCopyCurrentNetworkInfo.argtypes=[c_void_p]
c.CNCopyCurrentNetworkInfo.restype=c_void_p
ifs=c.CNCopySupportedInterfaces()
ifs=ObjCInstance(ifs)
for ifnam in ifs:
	info=ObjCInstance(c.CNCopyCurrentNetworkInfo(ifnam))
	if info['SSID']:
		WIFIname=str(info['SSID'])

