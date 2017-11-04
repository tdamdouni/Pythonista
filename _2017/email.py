# -*- coding: utf-8 -*-
# https://forum.omz-software.com/topic/4477/problem-to-send-an-email-using-mime

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

fromaddr = '''my mail adress'''
classe=input('enter the class: ts ou sec ou spe')
if classe=="ts":
  toaddrs='''list of the mail adresses'''
  filenames = '''list of my files'''
  paths='''list of the paths of the files like : \users\jean......'''
  n=len(paths)
if classe=='sec':
  toaddrs='''list of the mail adresses'''
  filenames = '''list of my files'''
  paths='''list of the paths of the files like : \users\jean......'''
  n=len(paths)
if classe=="spe":
    toaddrs='''list of the mail adresses'''
  filenames = '''list of my files'''
  paths='''list of the paths of the files like : \users\jean......'''
  n=len(paths)

for k in range(n):
  msg = MIMEMultipart()
  msg['From'] = fromaddr
  msg['To'] = toaddrs[k]
  msg['Subject'] = '''the subject'''
  body = '''body of the mail'''
  msg.attach(MIMEText(body, 'plain'))
  attachment = open(paths[k], "rb")
  filename=filenames[k]
  toaddr=toaddrs[k]
  part = MIMEBase('application', 'octet-stream')
  part.set_payload((attachment).read())
  encoders.encode_base64(part)
  part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
  msg.attach(part)
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(fromaddr, '''my password''')
  text = msg.as_string()
  server.sendmail(fromaddr, toaddr, text)
  server.quit()
