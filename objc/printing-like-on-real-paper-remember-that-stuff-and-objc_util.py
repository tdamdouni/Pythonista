# coding: utf-8

# https://forum.omz-software.com/topic/2936/printing-like-on-real-paper-remember-that-stuff-and-objc_util/2

# crashes
from objc_util import *

content = ns('<h1>test</h1>content')
html = ObjCClass('UIMarkupTextPrintFormatter').alloc().initWithMarkupText_(content)

# --------------------

# Most UIKit classes need to be used from the main thread.

from objc_util import *

@on_main_thread
def main():
	content = ns('<h1>test</h1>content')
	html = ObjCClass('UIMarkupTextPrintFormatter').alloc().initWithMarkupText_(content)
	
main()
# --------------------

