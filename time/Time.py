# coding: utf-8

# https://gist.github.com/S0n1cDev/faba08ac38578b7a65fd

from objc_util import *
import console
from time import localtime, strftime

def alert(message):
	alert_result=console.alert('Time', str(message),
	button1='Dismiss',hide_cancel_button=True)
	return
alert(strftime("%a, %d %b %Y %I:%M:%S +0000", localtime()));

