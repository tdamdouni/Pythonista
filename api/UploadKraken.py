# coding: utf-8

# https://www.macstories.net/reviews/pythonista-2-0-brings-action-extension-ipad-pro-support-code-editor-improvements-and-more/

from __future__ import print_function
import requests
import json
import appex
import datetime
import clipboard
import keychain
import photos
import console

timestamp = datetime.datetime.now()
name = timestamp.strftime("%Y-%m-%d-%H%M%S") + '.jpeg'

apiKey = 'YOUR_API_KEY'
apiSecret = 'YOUR_API_SECRET'

params = {
    'auth': {
        'api_key': apiKey,
        'api_secret': apiSecret
    },
    'wait': True,
        "convert": {
    "format": "jpeg"
  }
}

data = json.dumps(params)

if appex.is_running_extension() is True:
	image = appex.get_image_data()
else:
	image = photos.pick_image(original=True, raw_data=True)
	
print('Uploading to Kraken...')
console.show_activity()

request = requests.post(
    url = 'http://api.kraken.io/v1/upload',
    files = { 'name': (name, image)},
    data = { 'data': data }
)

response = json.loads(str(request.content))

if (response['success']):
	console.hud_alert('Lossless image uploaded to Kraken.', 'success')
else:
	print('Fail. Error message: %s ' % response['error'])
	
from Kraken import kraken
final = kraken(response['kraked_url'])

clipboard.set(final)
import urllib, cStringIO, Image

file = cStringIO.StringIO(urllib.urlopen(final).read())
img = Image.open(file)
img.show()

