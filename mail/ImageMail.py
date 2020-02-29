from __future__ import print_function
# Example for sending an email with an attached image using smtplib
#
# IMPORTANT: You need to enter your email login in the main() function.
#            The example is prepared for GMail, but other providers
#            should be possible by changing the mail server.

import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import Image
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
	to = 'example@example.com'
	subject = 'Image from Pythonista'
	gmail_user = 'YOUR_GMAIL_ADDRESS'
	gmail_pwd = 'YOUR_PASSWORD'
	
	#Load a sample image, modify as needed:
	image = Image.open('Test_Lenna')
	
	print('Connecting...')
	smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
	
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
	print('Done.')
	
if __name__ == '__main__':
	main()

