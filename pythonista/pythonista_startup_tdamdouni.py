# coding: utf-8

# https://forum.omz-software.com/topic/2397/feature-request-hooks-callbacks-into-some-pythonista-s-interface

# @omz

# I like to be a bit cautious with this type of functionality because it's potentially a pretty big maintenance burden when I make internal changes in the editor etc...

# There are already some fun things you can do with objc_util though. As an example, here's a script that appends to a Scrapbook.txt file every time you copy something to the clipboard (with a timestamp). If you'd include this in pythonista_startup.py, it comes pretty close to built-in functionality.

from objc_util import *

def pasteboardChanged_(_self, _cmd, _n):
	import clipboard
	from datetime import datetime
	import editor
	if editor.get_path().endswith('/Scrapbook_iPhone.txt'):
		# Don't add to ScrapBook when copying from it...
		return
	timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d - %H:%M')
	text = clipboard.get()
	with open('Scrapbook_iPhone.txt', 'a') as f:
		f.write('\n\n=== %s\n%s' % (timestamp, text))
		
try:
	Observer = ObjCClass('ScrapbookPasteboardObserver')
	# Observer was already created, don't do anything...
except ValueError:
	NSNotificationCenter = ObjCClass('NSNotificationCenter')
	UIPasteboard = ObjCClass('UIPasteboard')
	Observer = create_objc_class('ScrapbookPasteboardObserver', methods=[pasteboardChanged_])
	obs = Observer.new()
	NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(obs, sel('pasteboardChanged:'), 'UIPasteboardChangedNotification', UIPasteboard.generalPasteboard())
	
# https://forum.omz-software.com/topic/2535/fixing-the-caret-color-in-the-console-prompt

from objc_util import *
#Thanks to @JonB, he posted similar code a while back
def filter_subviews_by_class(view,objcclasstext=None):
	matching_svs=[]
	sv=view.subviews()
	if sv is None:
		return matching_svs
	for v in sv:
		if objcclasstext and objcclasstext in v._get_objc_classname():
			matching_svs.append(v)
		matching_svs.extend(
		filter_subviews_by_class(v,objcclasstext))
	return matching_svs
	
w=ObjCClass('UIApplication').sharedApplication().keyWindow()
main_view=w.rootViewController().view()
console_prompt=filter_subviews_by_class(main_view,'PA2PromptTextField')[0]
console_prompt.tintColor=ObjCClass('UIColor').colorWithRed_green_blue_alpha_(0.47, 0.67, 0.71, 1.0)

