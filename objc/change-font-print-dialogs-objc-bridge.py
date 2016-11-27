# https://forum.omz-software.com/topic/3687/share-string-text-to-real-printer-from-app/6

# @omz

from objc_util import *

@on_main_thread
def print_text(text, font_name='Helvetica', font_size=12):
	UIPrintInteractionController = ObjCClass('UIPrintInteractionController')
	UIPrintSimpleTextFormatter = ObjCClass('UISimpleTextPrintFormatter')
	controller = UIPrintInteractionController.sharedPrintController()
	formatter = UIPrintSimpleTextFormatter.alloc().initWithText_(text)
	font = ObjCClass('UIFont').fontWithName_size_(font_name, font_size)
	if font:
		formatter.setFont_(font)
	controller.setPrintFormatter_(formatter)
	controller.presentAnimated_completionHandler_(True, None)
	
print_text('Hello World', 'Courier', 10)

