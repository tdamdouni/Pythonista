# https://github.com/lukaskollmer/pythonista

"""
read and save custom preferences
and access those used by Pythonista
"""

__author__ = "Lukas Kollmer<lukas.kollmer@gmail.com>"
__copyright__ = "Copyright (c) 2016 Lukas Kollmer<lukas.kollmer@gmail.com>"

from pythonista import _utils
_utils.guard_objc_util()

import objc_util

NSUserDefaults = objc_util.ObjCClass("NSUserDefaults")

# legacy
#prefs_path = "/private/var/mobile/Containers/Data/Application/E299F4C9-A58C-4077-AA21-AC52DF94187F/Library/Preferences/com.omz-software.Pythonista3.plist"


def get(key):
	return NSUserDefaults.standardUserDefaults().objectForKey_(key)

def set(key, value):
	defaults = NSUserDefaults.standardUserDefaults()
	defaults.setObject_forKey_(value, key)
	defaults.synchronize()

def _debug():
	print(NSUserDefaults.standardUserDefaults().dictionaryRepresentation())

if __name__ == "__main__":
	_debug()
	print(get("EditorActionInfos"))
	print(get("RecentFiles"))
	print(get("EditorFontName"))
