# coding: utf-8

# https://forum.omz-software.com/topic/2936/printing-like-on-real-paper-remember-that-stuff-and-objc_util/4

from objc_util import *

@on_main_thread
def main():
	printContents = ns('<h1>test</h1>This is a test print page.')
	html = ObjCClass('UIMarkupTextPrintFormatter').alloc().initWithMarkupText_(printContents)
	printController = ObjCClass('UIPrintInteractionController').sharedPrintController()
	printController.setPrintFormatter_(html)
	def completion(_controller, completed, _error):
		pass
	completionHandler = ObjCBlock(completion, argtypes=[c_void_p, c_bool, c_void_p])
	#def completion(completed, _error):
		#pass
	#completionHandler = ObjCBlock(completion, argtypes = [c_bool, c_void_p])
	printController.presentAnimated_completionHandler_(0, completionHandler)
	
main()

# @omz, If you actually need the completion block to do something, your code is almost correct, the block is simply missing the first argument, which is a pointer to the UIPrintInteractionController itself, so it should be something like this (not tested):

