# https://github.com/lukaskollmer/pythonista

"""
Use this module to read/modify the editor wrench menu actions
"""

__author__ = "Lukas Kollmer<lukas.kollmer@gmail.com>"
__copyright__ = "Copyright (c) 2016 Lukas Kollmer<lukas.kollmer@gmail.com>"

from pythonista import defaults
import os

import objc_util

def get():
	_actions = []
	for action in defaults.get("EditorActionInfos"):
		keys = map(str, action.allKeys())
		values = map(str, action.allValues())
		_actions.append(dict(zip(keys, values)))
	return _actions

def add(action, index=-1):
	assert isinstance(action, dict), "The new action should be a dictionary"
	assert action["scriptName"], "The new action must contain a script to run"
	
	script_name = action["scriptName"]
	icon = action.get("iconName", "python")
	iconColor = action.get("iconColor", None)
	arguments = action.get("arguments", None)
	title = action.get("title", os.path.split(script_name)[1])
	
	new_action = {
		"scriptName": script_name,
		"iconName": icon,
		"arguments": arguments,
		"iconColor": iconColor,
		"title": title
	}
	
	if new_action["iconColor"] is None: del new_action["iconColor"]
	if new_action["arguments"] is None: del new_action["arguments"]
	
	current_actions = defaults.get("EditorActionInfos").mutableCopy()
	if index == -1:
		_index = current_actions.count()
	else:
		_index = index
	current_actions.insert(Object=objc_util.ns(new_action), atIndex=_index)
	defaults.set("EditorActionInfos", current_actions)

if __name__ == "__main__":
	for action in get():
		print(action)
	
	new_action = {
		"scriptName": "/Projects/File Browser/File Browser.py"
	}
	add(new_action)
