from __future__ import print_function
# http://www.macstories.net/links/quickly-email-a-picture-on-ios-using-pythonista/
# http://6d1f0d2e5a9f9c27cec8-28b934f7b0292a7dfd0ff5946ebc82f1.r53.cf1.rackcdn.com/2012-11-14_221033-ImageMail.py
# Example for sending an email with an attached image using smtplib
# 
# IMPORTANT: You need to enter your email login in the main() function.
#            The example is prepared for GMail, but other providers
#            should be possible by changing the mail server.

import smtplib
import sound
sound.load_effect('Bleep')
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import Image
import clipboard
import console
import keychain
from io import BytesIO

def get_attachment(img):
	bytes = BytesIO()
	img.save(bytes, format='JPEG')
	msg = MIMEBase('image', 'jpeg')
	msg.set_payload(bytes.getvalue())
	encoders.encode_base64(msg)
	msg.add_header('Content-Disposition', 'attachment',
	               filename='image.jpeg')
	return msg

def main():
	### CHANGE THESE VALUES:
	to = console.input_alert('Send Email To', 'Enter an email address below')
	subject = console.input_alert('Subject', 'Enter the subject of the email below')
	gmail_pwd = keychain.get_password('Gmail','your@email.com')
	gmail_user = 'your@email.com'
	
	#Load a sample image, modify as needed:
	image = clipboard.get_image()
	
	print('Connecting...')
	smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
	console.show_activity()
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail_user, gmail_pwd)
	
	print('Preparing message...')
	outer = MIMEMultipart()
	outer['Subject'] = subject
	outer['To'] = to
	outer['From'] = gmail_user
	outer.preamble = 'You will not see this in a MIME-aware email reader.\n'
	attachment = get_attachment(image)
	outer.attach(attachment)
	composed = outer.as_string()
	
	print('Sending...')
	smtpserver.sendmail(gmail_user, to, composed)
	smtpserver.close()
	console.hide_activity()
	sound.play_effect('Bleep')
	print('Done.')

if __name__ == '__main__':
	main()