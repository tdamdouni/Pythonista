# https://forum.omz-software.com/topic/3691/preparation-for-xcode-delete-files-in-pythonistaapptemplate/12

import inspect
import importlib

pyt_mods = [
        "os",
        "datetime",
        "json",
        "requests",
        "operator",
        "time",
        ]

pythonista_mods = [
        "ui",
        "console",
        "dialogs",
        "objc_util"
      ]

all_mods = pyt_mods + pythonista_mods

keep_list = []
for imods in all_mods:
	try:
		module_obj  = importlib.import_module(imods)
		filepath = inspect.getfile(module_obj).split("PythonistaKit.framework")[1]
		keep_list.append(filepath)
		
	except TypeError as e:
		print(e)
		
for filep in keep_list:
	print(filep)

