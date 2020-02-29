# coding: utf-8

# https://forum.omz-software.com/topic/3001/accessing-obj-c-help

from __future__ import print_function
import objc_util

# NSArray *apps = [[LSApplicationWorkspace defaultWorkspace] allInstalledApplications];

appWorkspace = ObjCClass('LSApplicationWorkspace')
default = (appWorkspace.defaultWorkspace())
apps = list(default.allInstalledApplications())
for app in apps:
	print(app)
	#print app.applicationIdentifier()

