# coding: utf-8

# https://github.com/HeyItsJono/Pythonista

# A script which, when run, will take the image on the clipboard, upload it to Imgur, then copy a direct link to the image to the clipboard automatically. This makes sharing images over any messaging service easy. Use the Pythonista Homescreen Shortcut Maker ( http://omz-software.com/pythonista/shortcut/ ) to make this a one click process.

from __future__ import print_function
import clipboard
import json
import requests
import base64
import sys
import os
import datetime
import notification
from PIL import Image
from console import hud_alert

API_KEY = "6fc84ae9833a1b66fb5d7e171cdbe71d204fc41a"
CLIENT_ID = "2693d5d109271c9"
headers = {"Authorization": "Client-ID {0}".format(CLIENT_ID)}
url = "https://api.imgur.com/3/upload.json"

img = clipboard.get_image(idx=0)

def main():
	try:
		img.save("pymgur_tmp.png", 'PNG')
	except AttributeError:
		print("There is no image on the clipboard'")
		sys.exit()
	f = open("pymgur_tmp.png", "rb")
	binary_data = f.read()
	b64image = base64.b64encode(binary_data)
	f.close()
	os.remove("pymgur_tmp.png")
	payload = {'key': API_KEY,
	           'image': b64image,
	           'type': 'base64',
	           'title': 'Pymgur Upload {}'.format(datetime.datetime.today().strftime("%c"))
	           }
	print("Uploading...")
	try:
		r = requests.post(url, headers = headers, data = payload)
	except requests.ConnectionError:
		hud_alert('No internet connection', icon = 'error')
		sys.exit()
	j = json.loads(r.text)
	link = j["data"]["link"]
	clipboard.set(link)
	hud_alert('Link Copied!')
	notification.schedule("Pymgur Upload Complete!", delay=0, action_url=link)
	print("The image link ({}) has been copied to the clipboard!".format(link))

if __name__ == "__main__":
	main()