# coding: utf-8

# https://www.macstories.net/reviews/pythonista-2-0-brings-action-extension-ipad-pro-support-code-editor-improvements-and-more/

from __future__ import print_function
import urllib
import urllib2
import json
import console
import keychain

apiKey = 'YOUR_API_KEY'
apiSecret = 'YOUR_API_SECRET'
rackspaceApi = 'YOUR_RACKSPACE_API_KEY'

def kraken(image_link):
	params = {
	'auth': {
	'api_key': apiKey,
	'api_secret': apiSecret
	},
	'url': image_link,
	'wait': True,
	"cf_store": {
	"user": "macstories",
	"key": rackspaceApi,
	"container": "Kraken",
	"ssl": True
	},
	'lossy': True # Set lossy upload because UploadKraken.py doesn't upload as lossy first. This lets you compare image savings with the original image later.
	}
	
	url = 'https://api.kraken.io/v1/url'
	
	console.hud_alert('Uploading lossy image to Kraken...', 'success')
	data = json.dumps(params)
	request = urllib2.Request(url, data)
	response = urllib2.urlopen(request)
	jsonRes = json.loads(str(response.read()))
	
	if (jsonRes['success']):
		print('Success. Saved ' + str((jsonRes['original_size']-jsonRes['kraked_size'])/1000) + 'kb in total.' + '\n' + 'Optimized image URL: ' + jsonRes['kraked_url'])
		return jsonRes['kraked_url']
	else:
		print('Fail. Error message: %s ' % jsonRes['error'])
		
		
def main():
	# If not called by other script, get image link from iOS clipboard.
	import clipboard
	image_link = clipboard.get()
	final = kraken(image_link)
	clipboard.set(final)
	
if __name__ == '__main__':
	main()

