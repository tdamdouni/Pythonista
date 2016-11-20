# coding: utf-8

# https://forum.omz-software.com/topic/2796/dark-keyboard-for-ui-textfield-textview/2 

import ui
from objc_util import ObjCInstance, on_main_thread

@on_main_thread
def set_kb_apperance(view, appearance='dark'):
	a = 1 if appearance == 'dark' else 0
	if isinstance(view, ui.TextView):
		ObjCInstance(tv).setKeyboardAppearance_(a)
	elif isinstance(view, ui.TextField):
		ObjCInstance(view).subviews()[0].setKeyboardAppearance_(a)
	else:
		raise TypeError('Expected ui.TextView or ui.TextField')

