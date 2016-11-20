# coding: utf-8

# https://github.com/lukaskollmer/pythonista-scripts/blob/master/ImportObjcClass/ImportObjCClass.py

# Put this script into the editor action (wrench) menu.
# Whenever you want to import an Objective-C class,
# you jutst need to  type the classname, select it and invoke this script via the action menu.
# This script will check if a classname with the name you selected exists
# and add ` = ObjcClass(_classname_)` to the end of the line

import editor, console, sys
from objc_util import ObjCClass

selection = editor.get_selection()
line = editor.get_line_selection()

text = editor.get_text()

classname = text[int(selection[0]):int(selection[1])]

try:
	ObjCClass(classname)
	editor.set_selection(selection[1])
	editor.replace_text(selection[1], selection[1], ' = ObjCClass(\'{}\')'.format(classname))
except:
	console.hud_alert(sys.exc_info()[1].message, 'error')

