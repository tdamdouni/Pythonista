# https://gist.github.com/lukaskollmer/0c01b7a27e512db480847fac2cc54103

# in association with script custom-editor-font

# https://forum.omz-software.com/topic/3419/share-code-custom-editor-font

"""
Use custom fonts in the editor

Usage: https://forum.omz-software.com/topic/3419/share-code-custom-editor-font
"""

__author__ = "Lukas Kollmer<lukas.kollmer@gmail.com>"
__copyright__ = "Copyright (c) 2016 Lukas Kollmer<lukas.kollmer@gmail.com>"

from objc_util import *
from ctypes import *


CTFontManagerRegisterFontsForURL = c.CTFontManagerRegisterFontsForURL
CTFontManagerRegisterFontsForURL.argtypes = [c_void_p, c_int, c_void_p]
CTFontManagerRegisterFontsForURL.restype = c_bool

CFURLCreateWithString = c.CFURLCreateWithString
CFURLCreateWithString.argtypes = [c_void_p, c_void_p, c_void_p]
CFURLCreateWithString.restype = c_void_p



def load_custom_font(file):
	#https://marco.org/2012/12/21/ios-dynamic-font-loading
	font_url = CFURLCreateWithString(None, ns(file), None)
	
	error = c_void_p(None)
	# This returns false, but still succeds
	CTFontManagerRegisterFontsForURL(ObjCInstance(font_url), 0, byref(error))
	
def set_editor_font(name, size=15):
	"""
	NOTE: This still requires a restart
	"""
	defaults = ObjCClass("NSUserDefaults").standardUserDefaults()
	defaults.setObject_forKey_(name, "EditorFontName")
	defaults.setObject_forKey_(size, "EditorFontSize")
	
	defaults.synchronize()
	
def reset_custom_font():
	defaults = ObjCClass("NSUserDefaults").standardUserDefaults()
	defaults.setObject_forKey_("Menlo-Regular", "EditorFontName")
	defaults.setObject_forKey_(15, "EditorFontSize")
	
	
if __name__ == "__main__":
	import os
	font_path = "file://" + os.path.expanduser("~/Documents/Fonts/SFMono/SFMono-Regular.otf")
	
	load_custom_font(font_path)
	
	font_name = "Menlo-Regular"
	set_editor_font(font_name, 15)

