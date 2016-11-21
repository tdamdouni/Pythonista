# coding: utf-8

# http://stackoverflow.com/questions/27828997/trying-to-read-emails-from-gmail-using-pythonista

from __future__ import print_function
import getpass
import imaplib
import console
import collections
import re
import email
import codecs
import quopri

console.clear()
mail = imaplib.IMAP4_SSL('imap.gmail.com',993)
my password = getpass.getpass("Password: ")
address = 'sch.e@gmail.com'
print('Which email address (TO) would you like to search: ',end='')
EE = raw_input()
SS = r"(TO "+"\""+EE+"\""+r")"
mail.login(address, mypassword)
mail.select("inbox")  #select the box on gmail
print("Checking for e-mails TO ",EE)
typ, messageIDs = mail.search(None,'(SINCE "01-Jan-2014")',SS)
MIDs=messageIDs[0].split()
for mailid in MIDs[::-1]:
	resp, data = mail.fetch(mailid,'(RFC822)')
	raw_body=data[0][1]
	print(raw_body.decode('UTF-8','strict'))
	print(quopri.encodestring(raw_body))
	msg=email.message_from_string(raw_body)
	print(msg)
	
raw_body=data[0][1]
raw_body=quopri.decodestring(raw_body)
raw_body=raw_body.decode('ISO-8859-1')

