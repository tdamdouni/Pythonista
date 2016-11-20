# https://gist.github.com/audente/5414027

import smtplib 

class GMailServer:
  def __init__(self, username, password):
		self.server = smtplib.SMTP('smtp.gmail.com:587')  
		self.server.starttls()  
		self.server.login(username,password)
		
	def __enter__(self):
		return self.server
		
	def __exit__(self, type, value, traceback):
		self.server.quit()

# --------------------------------------------------
from email.mime.text import MIMEText

def SendMail(server, fromaddr, toaddr, subject, body):

	msg = MIMEText(body)

	msg['Subject'] = subject
	msg['From'] = fromaddr
	msg['To'] = toaddr

	server.sendmail(fromaddr, [toaddr], msg.as_string())

# --------------------------------------------------
'''

fromaddr = 'fromaddr@gmail.com'  
toaddrs  = 'toaddrs@gmail.com'  
subject  = 'subject'
body = 'body text'    
  
# Credentials  
username = 'fromaddr@gmail.com'  
password = 'password' 
		
with GMailServer(username, password) as server:
	SendMail(server, fromaddr, toaddrs, subject, body)

'''
