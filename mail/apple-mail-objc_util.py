# coding: utf-8

# https://forum.omz-software.com/topic/3025/apple-mail-objc_util/5

from __future__ import print_function
from objc_util import *
import smtplib

# - (void)mailComposeController:(MFMailComposeViewController *)controller didFinishWithResult:(MFMailComposeResult)result error:(NSError *)error
def mailComposeController_didFinishWithResult_error_(_self, _cmd, controller, result, error):
	print('Mail composer finished')
	# Wrap the controller parameter in an `ObjCInstance`, so we can send messages:
	mail_vc = ObjCInstance(controller)
	# Set delegate to nil, and release its memory:
	mail_vc.setDelegate_(None)
	ObjCInstance(_self).release()
	# Dismiss the sheet:
	mail_vc.dismissViewControllerAnimated_completion_(True, None)
	
methods = [mailComposeController_didFinishWithResult_error_]
protocols = ['MFMailComposeViewControllerDelegate']
MyMailComposeDelegate = create_objc_class('MyMailComposeDelegate', NSObject, methods=methods, protocols=protocols)

@on_main_thread
def show_mail_sheet():
	MFMailComposeViewController = ObjCClass('MFMailComposeViewController')
	mail_composer = MFMailComposeViewController.alloc().init().autorelease()
	# Use our new delegate class:
	delegate = MyMailComposeDelegate.alloc().init()
	mail_composer.setDelegate_(delegate)
	# Present the mail sheet:
	root_vc = UIApplication.sharedApplication().keyWindow().rootViewController()
	root_vc.presentViewController_animated_completion_(mail_composer, True, None)
	
if __name__ == '__main__':
	show_mail_sheet()
	
# --------------------

#s = smtplib.SMTP('SMTP server ip')
#s.sendmail(me, me, msg.as_string())

# --------------------

