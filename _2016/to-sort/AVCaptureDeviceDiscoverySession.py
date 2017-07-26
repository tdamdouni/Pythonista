# https://forum.omz-software.com/topic/3555/casting-nsarray-from-objcinstancemethodproxy

from objc_util import *

AVCaptureDeviceDiscoverySession = ObjCClass('AVCaptureDeviceDiscoverySession')

types = ['AVCaptureDeviceTypeBuiltInDuoCamera' ,
         'AVCaptureDeviceTypeBuiltInWideAngleCamera',
         'AVCaptureDeviceTypeBuiltInTelephotoCamera']
session = AVCaptureDeviceDiscoverySession.discoverySession(deviceTypes=types, mediaType='vide', position=0)

devices = session.devices()
print(devices)

