# coding: utf-8

# https://gist.github.com/S0n1cDev/fcd639542dd5d4f12cb9

from objc_util import *
import console
import os
import sys

UIDevice = ObjCClass('UIDevice')

device = UIDevice.currentDevice()

def alert(message):
	alert_result=console.alert('iOS Device Version', str(message),
	button1='Dismiss',hide_cancel_button=True)
	return
alert(device.systemVersion());
