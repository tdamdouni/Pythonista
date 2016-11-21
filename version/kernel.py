# coding: utf-8

# https://forum.omz-software.com/topic/2866/i-cannot-seem-to-get-os-uname-in-a-console-alert/2

import os
import sys
import console

#def uname():
	#os.uname()

def alert(message):
	alert_result=console.alert('Kernel/uname info',str(message), button1='Dismiss',hide_cancel_button=True)
	return
alert(os.uname())

