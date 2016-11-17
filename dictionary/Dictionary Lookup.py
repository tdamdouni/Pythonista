# coding: utf-8

# https://github.com/lukaskollmer/pythonista-scripts/blob/master/ios-dictionary/Dictionary%20Lookup.py

# https://forum.omz-software.com/topic/3016/access-to-apple-standard-language-dictionaries

from objc_util import ObjCClass, UIApplication, CGSize, on_main_thread
import sys
import appex
import dialogs
import ui

UIReferenceLibraryViewController = ObjCClass('UIReferenceLibraryViewController')


@on_main_thread
def main():
	if len(sys.argv) > 1:
		input = ' '.join(sys.argv[1:])
	else:
		input = dialogs.text_dialog()
	if input:
		referenceViewController = UIReferenceLibraryViewController.alloc().initWithTerm_(input)
		
		rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
		tabVC = rootVC.detailViewController()
		
		referenceViewController.setTitle_('Definition: {0}{1}{0}'.format('\'', input))
		referenceViewController.setPreferredContentSize_(CGSize(540, 540))
		referenceViewController.setModalPresentationStyle_(2)
		
		#tabVC.addTabWithViewController_(referenceViewController)
		tabVC.presentViewController_animated_completion_(referenceViewController, True, None)

if __name__ == '__main__':
	if not appex.is_running_extension():
		main()
	else:
		dialogs.hud_alert('Script does not work in app extension', icon='error')
