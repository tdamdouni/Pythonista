#!/usr/local/bin/python2.7

# coding: utf-8

# https://gist.github.com/Moving-Electrons/8387168

# This Python script checks stock prices in Google Finance pages and send notifications (email and instant) if predetermined conditions in a csv file (passed as argument) are met. More info in: www.movingelectrons.net/blog/2014/1/12/how-to-get-alerts-on-stock-price-changes-using-python

from __future__ import print_function
import string, re, os, time, smtplib, sys
from urllib import urlopen
import httplib, urllib #used in the Pushover code


def quote_grab(symbol):

	baseurl = 'http://google.com/finance?q='
	urlData = urlopen(baseurl + symbol)
	
	print('Opening Google Finance URL...')
	
	# Another option: namestr = re.compile('.*name:\"' + symbol + '\",cp:(.*),p:(.*?),cid(.*)}.*')
	namestr = re.compile('.*name:\"' + symbol + '\",cp:(.*),p:(.*?),cid(.*)') # "?" used as there is a second string "cid" in the page and the Match was being done up to that one. The "?" keeps it to the 1st occurrence.
	
	print('Checking quotes for ' + symbol)
	
	for line in urlData:
	
		m = re.match(namestr, line)
		
		if m:
			#Since the method m.group(2) returns a string in the form "xxxx", it cannot be converted to float,
			#therefore I strip the "" from that string and pass it to the float function.
			priceStr = m.group(2).strip('"')
			price = float(priceStr)
			
			
	urlData.close()
	return price #returns price as a float
	
def pushover(msg):

	conn = httplib.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
	urllib.urlencode({
	"token": "INSERT YOUR TOKEN HERE",
	"user": "INSERT YOUR API USER KEY HERE",
	"message": msg,
	}), { "Content-type": "application/x-www-form-urlencoded" })
	conn.getresponse()
	
	
def send_email(sbjt, msg):
	fromaddr = 'INSERT HERE THE FROM EMAIL ADDRESS'
	toaddrs = 'INSERT THE EMAIL ADDRESS THE NOTIFICATION WILL BE SENT TO'
	bodytext = 'From: %s\nTo: %s\nSubject: %s\n\n%s' %(fromaddr, toaddrs, sbjt, msg)
	
	# Credentials (if needed)
	username = 'USERNAME@gmail.com'
	password = 'INSERT HERE YOUR PASSWORD'
	
	# The actual mail sent
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, bodytext)
	server.quit()
	
#------------------------
# Constants
file = sys.argv[1]

#------------------------

# Opens .cvs file, gets string at last line, converts it to list so that the comparison in the
# IF statement below can be done
csvFile = open(file, 'r')
body = 'Changes:\n'
chg = False

for line in csvFile:
	linelst = line.split(',')
	quote = quote_grab(linelst[0])
	
	if quote>float(linelst[1]) and linelst[2]==('a\n' or 'a'):
		body = body + 'Price for %s went up to %s (threshold = %s)\n' % (linelst[0], quote, linelst[1])
		chg = True
	if quote<float(linelst[1]) and linelst[2]==('b\n' or 'b'):
		body = body + 'Price for %s went down to %s (threshold = %s)\n' % (linelst[0], quote, linelst[1])
		chg = True
		
if chg:
	print('sending email...')
	send_email('Stock Price Changes',body)
	print('sending message to pushover...')
	pushover(body)
	
csvFile.close()

