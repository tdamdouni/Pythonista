# coding: utf-8

# https://gist.github.com/S0n1cDev/a100952e1cc5decc5935

import os
import sys
import console
import platform
def alert(message):
	alert_result=console.alert('Kernel version', str(message),
	button1='Dismiss',hide_cancel_button=True)
	return
alert(platform.version());
