from __future__ import print_function
# IMPORTANT: You need to enter your email login in the main() function.
#            The example is prepared for GMail, but other providers
#            should be possible by changing the mail server.

import smtplib
from email.mime.multipart import MIMEMultipart
from email import encoders
import sys
import webbrowser
import console
import keychain
from base64 import b64decode

def main():

	tasks = sys.argv[1].splitlines()
	
	### CHANGE THESE VALUES:
	
	# My login script -- you'll need to delete / comment this and add your info below.
	to = keychain.get_password('omnifocus','maildrop_address')
	
#       to = 'Your_OmniGroup_MailDrop_Address'
#   gmail_user = 'Your_Email@gmail.com' # comment my b64 stuff in the next line
	gmail_user = b64decode('bjhoZW5yaWVAZ21haWwuY29t')
	gmail_pwd = keychain.get_password('multilineomnifocus',gmail_user)
	
	console.clear()
	print('Starting SMTP Server')
	
	smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail_user, gmail_pwd)
	
	for task in tasks:
		outer = MIMEMultipart()
		outer['Subject'] = task
		outer['To'] = to
		outer['From'] = gmail_user
		outer.preamble = 'You will not see this in a MIME-aware email reader.\n'
		
		composed = outer.as_string()
		
		print('Sending Task ' + str(tasks.index(task) + 1))
		smtpserver.sendmail(gmail_user, to, composed)
		
	smtpserver.close()
	print('Done')
	console.clear()
	
	# Added to kind of support callbacks while maintaining
	# backwards compatibility.
	return_to = sys.argv[-1]
	
	if len(sys.argv) > 2 and webbrowser.open(return_to):
		webbrowser.open(return_to)
	else:
		webbrowser.open('drafts:')
		
if __name__ == '__main__':
	main()

