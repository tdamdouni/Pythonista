# https://forum.omz-software.com/topic/3687/share-string-text-to-real-printer-from-app/3

# @omz

from objc_util import *

@on_main_thread
def print_text(text):
	UIPrintInteractionController = ObjCClass('UIPrintInteractionController')
	UIPrintSimpleTextFormatter = ObjCClass('UISimpleTextPrintFormatter')
	controller = UIPrintInteractionController.sharedPrintController()
	formatter = UIPrintSimpleTextFormatter.alloc().initWithText_(text).autorelease()
	controller.setPrintFormatter_(formatter)
	controller.presentAnimated_completionHandler_(True, None)
	
print_text('Hello World')

