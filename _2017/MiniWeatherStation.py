#!/usr/bin/python

import json
import sys
import time
import datetime

# libraries
import sys
import urllib2
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from sense_hat import SenseHat

# Oauth JSON File
GDOCS_OAUTH_JSON       = 'Mini Weather Station-f68343d4a35a.json'

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'Sense HAT Logs'

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 30


def login_open_sheet(oauth_key_file, spreadsheet):
	"""Connect to Google Docs spreadsheet and return the first worksheet."""
	try:
		json_key = json.load(open(oauth_key_file))
		credentials = SignedJwtAssertionCredentials(json_key['client_email'],
													json_key['private_key'],
													['https://spreadsheets.google.com/feeds'])
		gc = gspread.authorize(credentials)
		worksheet = gc.open(spreadsheet).sheet1
		return worksheet
	except Exception as ex:
		print 'Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!'
		print 'Google sheet login failed with error:', ex
		sys.exit(1)


sense = SenseHat()
sense.clear()		
print 'Logging sensor measurements to {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS)
print 'Press Ctrl-C to quit.'
worksheet = None
while True:
	# Login if necessary.
	if worksheet is None:
		worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)

	# Attempt to get sensor reading.
	temp = sense.get_temperature()
	temp = round(temp, 1)
	humidity = sense.get_humidity()
	humidity = round(humidity, 1)
	pressure = sense.get_pressure()
	pressure = round(pressure, 1)
	
	# 8x8 RGB
	sense.clear()
	info = 'Temperature (C): ' + str(temp) + 'Humidity: ' + str(humidity) + 'Pressure: ' + str(pressure)
	sense.show_message(info, text_colour=[255, 0, 0])
	
	# Print
	print "Temperature (C): ", temp
	print "Humidity: ", humidity
	print "Pressure: ", pressure, "\n"

	# Append the data in the spreadsheet, including a timestamp
	try:
		worksheet.append_row((datetime.datetime.now(), temp,humidity,pressure))
	except:
		# Error appending data, most likely because credentials are stale.
		# Null out the worksheet so a login is performed at the top of the loop.
		print 'Append error, logging in again'
		worksheet = None
		time.sleep(FREQUENCY_SECONDS)
		continue

	# Wait 30 seconds before continuing
	print 'Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME)
	time.sleep(FREQUENCY_SECONDS)
