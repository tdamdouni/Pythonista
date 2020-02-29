# coding: utf-8

# https://gist.github.com/filippocld/bc3421de03cb3db40be5

# https://forum.omz-software.com/topic/2477/is-my-device-jailbroken

from __future__ import print_function
import os
jailbroken=True
try:
	os.chdir('/private')
	os.listdir('.')
except OSError:
	jailbroken=False
	
print('Is my device jailbroken: '+ str(jailbroken))

