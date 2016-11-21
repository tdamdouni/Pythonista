# coding: utf-8

# https://forum.omz-software.com/topic/2936/printing-like-on-real-paper-remember-that-stuff-and-objc_util

from objc_util import *

content = ns('<h1>test</h1>content')
html = ObjCClass('UIMarkupTextPrintFormatter').alloc().initWithMarkupText_(content)

# --------------------

from objc_util import *

@on_main_thread
def main():
	content = ns('<h1>test</h1>content')
	html = ObjCClass('UIMarkupTextPrintFormatter').alloc().initWithMarkupText_(content)
	
main()

# --------------------

# coding: utf-8

from objc_util import *

@on_main_thread
def main():
	printContents = ns('<h1>test</h1>This is a test print page.')
	html = ObjCClass('UIMarkupTextPrintFormatter').alloc().initWithMarkupText_(printContents)
	printController = ObjCClass('UIPrintInteractionController').sharedPrintController()
	printController.setPrintFormatter_(html)
	def completion(completed, _error):
		pass
	completionHandler = ObjCBlock(completion, argtypes = [c_bool, c_void_p])
	printController.presentAnimated_completionHandler_(0, completionHandler)
	
main()

# --------------------

def completion(_controller, completed, _error):
	pass
	
completionHandler = ObjCBlock(completion, argtypes=[c_void_p, c_bool, c_void_p])
# ...

# --------------------

printInfo = ObjcClass('UIPrintInfo').printInfoWithDictionary_(None)

printInfo.orientation = #here's where we have problems...
#in Objc it is just printInfo.orientation = UIPrintInfoOrientationLandscape
#or printInfo.orientation = UIPrintInfoOrientationPortrait
#I know it will default to portrait, but in particular I want to be able to set it to Landscape.

printController.printInfo = printInfo

# --------------------

typedef enum {
   UIPrintInfoOrientationPortrait,
   UIPrintInfoOrientationLandscape,
} UIPrintInfoOrientation;

# --------------------

