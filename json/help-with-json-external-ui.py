# coding: utf-8

# https://forum.omz-software.com/topic/3083/help-with-json-external-ui/2

from __future__ import print_function
import os, json

def loadsettings(file):
	if os.path.exists(file):
		with open(file, "r") as f:
			return json.load(f)
			
file = "test.pyui"
settings = loadsettings(file)

i = 0
for s in settings[0]:    #show me dicts in list
	if s == 'nodes':
		print(s + ' = ', end=' ')
		for d in settings[0].values()[i]:
			print(d)
			print()
	else:
		print(s + ' = ' + str(settings[0].values()[i]))
		print()
	i += 1
	
print('get attributes of the first node:')
print("settings[0].get('nodes')[0].values()[0] = " + str(settings[0].get('nodes')[0].values()[0]))

