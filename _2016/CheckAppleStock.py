# https://gist.github.com/omarshahine/f8eb4598af4f1767ab1a9f01662e74b1

# If you don't have the requests module, you can download by typing:
#
# 	sudo easy_install -U requests`
#
# into the terminal on macOS
#
# You can change the partnum below with any Apple SKU
#

import urllib
import json
import requests

def get_status(zipcode):
	partnum = "MMEF2AM/A"
	print("===========================================")
	print ("Checking AirPods for "  + zipcode)
	print("===========================================")
	
	url = "http://www.apple.com/shop/retail/pickup-message?parts.0=" + (partnum) + "&location=" + zipcode
	
	r = requests.get(url)
	json = r.json()
	
	body = json['body']
	
	for store in body['stores']:
		status = store['partsAvailability']
		print (store['storeName'].ljust(20) + ": " + str(status[partnum]['pickupDisplay']).rjust(20))

get_status("98052")
