# https://github.com/lukaskollmer/pythonista/blob/master/pythonista/editor_util.py#L28

"""
Use this module to change the editor and console font programatically
"""

__author__ = "Lukas Kollmer<lukas.kollmer@gmail.com>"
__copyright__ = "Copyright (c) 2016 Lukas Kollmer<lukas.kollmer@gmail.com>"

from pythonista import _utils
from pythonista import defaults

_utils.guard_objc_util()

import objc_util
import ctypes

# --- Custom Fonts

UIFont = objc_util.ObjCClass("UIFont")
OMBarButton = objc_util.ObjCClass('OMBarButton')
UIButton = objc_util.ObjCClass('UIButton')



PA2UniversalTextEditorViewController = objc_util.ObjCClass("PA2UniversalTextEditorViewController")
PA2EmptyTabViewController = objc_util.ObjCClass("PA2EmptyTabViewController")


CTFontManagerRegisterFontsForURL = objc_util.c.CTFontManagerRegisterFontsForURL
CTFontManagerRegisterFontsForURL.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
CTFontManagerRegisterFontsForURL.restype = ctypes.c_bool

CFURLCreateWithString = objc_util.c.CFURLCreateWithString
CFURLCreateWithString.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
CFURLCreateWithString.restype = ctypes.c_void_p



def load_custom_font(file):
	#https://marco.org/2012/12/21/ios-dynamic-font-loading
	font_url = CFURLCreateWithString(None, objc_util.ns(file), None)
	
	error = ctypes.c_void_p(None)
	success = CTFontManagerRegisterFontsForURL(objc_util.ObjCInstance(font_url), 0, ctypes.byref(error))
	#print(objc_util.ObjCInstance(error))
	#print("success:", success)
	
	#font = UIFont.fontWithName_size_("SFMono-Regular", 15)
	#print(font)

def set_editor_font(name, size=15):
	"""
	NOTE: This still requires a restart
	"""
	defaults.set("EditorFontName", name)
	defaults.set("EditorFontSize", size)
	
	#font = objc_util.UIFont.fontWithName_size_(name, size)

# --- Custom Button Items

_DEFAULT_BAR_BUTTON_POSITION = "left"

UIBarButtonItem = objc_util.ObjCClass('UIBarButtonItem')

def _add_button_item(item, position=_DEFAULT_BAR_BUTTON_POSITION):
	"""
	Do not call this directly, it just adds the item to the view.
	You'll need to add the action to the view manually
	"""
	tabVC = _utils._application.keyWindow().rootViewController().detailViewController()
	
	if position == "left":
		buttonItems = tabVC.persistentLeftBarButtonItems().mutableCopy()
		buttonItems.insert(Object=item, atIndex=0)
		tabVC.setPersistentLeftBarButtonItems_(buttonItems)
		tabVC.reloadBarButtonItemsForSelectedTab()
	elif position == "right":
		toolbar = tabVC.toolbar()
		button = UIButton.new()
		button.setTitle_("title")
		toolbar.addSubview_(button)
	


def add_text_button_item(text, action, position=_DEFAULT_BAR_BUTTON_POSITION):
	tabVC = _utils._application.keyWindow().rootViewController().detailViewController()
	selector = _utils.add_method(action, tabVC)
	
	barButtonItem = UIBarButtonItem.alloc().init(Title=text, style=0, target=tabVC, action=selector)
	#print(barButtonItem)
	_add_button_item(barButtonItem, position)

def add_image_button_item(image, action, position=_DEFAULT_BAR_BUTTON_POSITION):
	barButtonItem = UIBarButtonItem.alloc().init(Image=image, style=0, target=tabVC, action=selector)
	#print(barButtonItem)
	_add_button_item(barButtonItem, position)


# --- Editor Keyboard Shortcuts
""" Moved to the `shortcuts` submodule """


# --- Tab Management
def close_tab(tab):
	if isinstance(tab, objc_util.ObjCInstance):
		if tab.isKindOfClass_(PA2UniversalTextEditorViewController):
			tabVC = _utils._application.keyWindow().rootViewController().detailViewController()
			tabVC.closeTab_(tab)
	if isinstance(tab, int):
		tabVC = _utils._application.keyWindow().rootViewController().detailViewController()
		tab = tabVC.tabViewControllers()[tab]
		print(tab)
		close_tab(tab)

def close_current_tab():
	import editor
	tab = editor._get_editor_tab()
	close_tab(tab)

def open_tab(path_or_index=None):
	tabVC = _utils._application.keyWindow().rootViewController().detailViewController()
	# Open a new empty tab
	if isinstance(path_or_index, type(None)):
		tabVC.addTab_(None)
	
	# Open a new tab with a file
	if isinstance(path_or_index, str):
		import editor
		#tabVC.open(File=path, inNewTab=True, withPreferredEditorType=True, forceReload=False)
		editor.open_file(path_or_index, new_tab=True, force_reload=False)
	
	# Switch to an existing tab
	if isinstance(path_or_index, int):
		# This doesn't really work well, since just the editor will change tab,
		# but Pythonista won't select a different tab in the tab bar
		#tabVC.selectTabAtIndex_(path)
		
		# from editor.py
		tabs = []
		for tab in tabVC.tabViewControllers():
			if tab.isKindOfClass_(PA2EmptyTabViewController):
				tabs.append(None)
			if tab.isKindOfClass_(PA2UniversalTextEditorViewController):
				if not tab.isViewLoaded():
					tabs.append(None)
					continue
				tab_path = str(tab.filePath())
				tabs.append(tab_path)
		
		path = tabs[path_or_index]
		if not path is None:
			import editor
			editor.open_file(path, new_tab=True, force_reload=False)
		else:
			raise ValueError("Can't open empty path")
		
	

# --- Quick Open

def show_quick_open():
	pass
	

# --- Demo
if __name__ == "__main__":
	
	# Test custom fonts
	import os
	font_path = "file://" + os.path.expanduser("~/Documents/Fonts/SFMono/SFMono-Regular.otf")
	
	#load_custom_font(font_path)
	
	font_name = "Menlo-Regular"
	#set_editor_font(font_name, 15)
	
	"""
	# Test bar buttons
	def button_action(_self, _sel):
		print("button tapped!!!")
	add_text_button_item("hi", button_action, "left")
	
	
	# Test keyboard shortcuts
	def commandGHandler(_self, _sel):
		print("Command G pressed")
	
	register_shortcut("cmd+g", commandGHandler, "")
	"""
	
	open_tab(2)
