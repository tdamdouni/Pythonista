# coding: utf-8

# https://gist.github.com/jsbain/f82be8d8840f86b387a4
import os
import objc_util
from objc_util import *
# setup an array of objects we cannot discard
objc_util.retain=getattr(objc_util,'retain',[])
root_vc = UIApplication.sharedApplication().keyWindow().rootViewController()

def mailComposeController_didFinishWithResult_error_(self, sel, controller, result, error):
	root_vc.dismissModalViewControllerAnimated_(True)
	objc_util.retain.remove(ObjCInstance(self))	

def show_mail_controller(subject='', recipients=[], body='', filename=None, mime_type=''):	
	'''show a mail controller, prepopulating with subject, recipients[must be list], body, 
           filename, and attachment mime type string, such as image/gif
	'''
	try:
		MailDelegate = ObjCClass('MailDelegate')
	except: #create new class
		MailDelegate=create_objc_class('MailDelegate',
			superclass=NSObject,   
                        methods=[mailComposeController_didFinishWithResult_error_],  
                        protocols=['MFMailComposeViewController'])
		#retain callback
		objc_util.retain.append(
			mailComposeController_didFinishWithResult_error_)
	MFMailComposeViewController=ObjCClass('MFMailComposeViewController')
	mail_vc=MFMailComposeViewController.alloc().init()
	delegate=MailDelegate.alloc().init().autorelease()
	objc_util.retain.append(delegate)
	#mail_vc.mailComposeDelegate=delegate
	#set message properties
	#mail_vc.setSubject_(subject)
	#if isinstance(recipients,list):
	# cclauss's comment 
	isHTML = isinstance(body, basestring) and body.strip().startswith('<html>')
	
	mail_vc.setToRecipients_(recipients)
	#isHTML = isinstance(body,basestring) and body.startswith('<html>'):
	isHTML=True
	mail_vc.setMessageBody_isHTML_(body,isHTML)
	if filename and os.path.exists(filename):
		mail_vc.addAttachmentData_mimeType_fileName_(
		NSData.dataWithContentsOfFile_(os.path.abspath(filename)),
		mime_type, filename )
	#present the controller
	root_vc.presentModalViewController_animated_(mail_vc,True)


def main():
	import ui
	import urllib
	urllib.urlretrieve('http://www.heathersanimations.com/fireworks/22_1.gif','test.gif')
	v=ui.View(bg_color=(1,1,1), frame=( 0,0,555,555))
	v.present()
	b=ui.Button(title='Mail', frame=(25,25,200,200))
	@ui.in_background
	def a(sender):
		v.close()  # if using a view, must close first
		show_mail_controller('Enlarge you gif! ', 
                   ['someone@somewhere.com'],'Try this amazing animated gif!', 'test.gif','image/gif')
	b.action=a
	v.add_subview(b)

if __name__=='__main__':
	main()
