# https://github.com/lukaskollmer/pythonista

"""
Access information about the Pythonista app

TODO:
	[]  badge
		[x] badge number
		[x] badge string (set)
		[]  badge string (get)
	[x] version
	[]  current interpreter
	[x] keyboard shortcuts 
	[]  themes (get and set)
	[x] browse documents folder
	[]  add script to home screen
	[x] edit wrench actions
	[x]  run a script of your choice
	[]  tab management
		[x] close current tab
		[x]  close tab by index
		[x]  close specific tab
		[x]  open new tab
		[x] open new empty tab
		[]  change tab
	[x]  Quick Open (like Xcode)
	[]  Some system where ui.Views can be closed using cmd+w

FIXME:
	[] dont set `tabVC` to UIApplication.sharedApplication().keyWindow().rootViewController()
"""
__author__ = "Lukas Kollmer<lukas.kollmer@gmail.com>"
__copyright__ = "Copyright (c) 2016 Lukas Kollmer<lukas.kollmer@gmail.com>"

from pythonista import badge
from pythonista import defaults
from pythonista import editor_util
from pythonista import files
from pythonista import interpreter
from pythonista import shortcuts
from pythonista import theme
from pythonista import version
from pythonista import wrenchmenu

