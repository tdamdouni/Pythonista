# coding: utf-8

# https://gist.github.com/philgruneich/13f02f45a41ad90f454f

# Requires Pythonista for iOS and Interact for iOS. Sends image and returns OCR'd text. Opens text in Interact unless used from action extension, then adds to clipboard.

from __future__ import print_function
import requests
import photos
from PIL import Image, ImageEnhance
import StringIO
import appex
import console
import json
import keychain

api_key = keychain.get_password('Project Oxford', 'Computer Vision API')

if api_key == None:
	import clipboard
	api_key = console.input_alert('Insert your API key', '', str(clipboard.get()))
	if api_key == None:
		raise Exception('You need an API key.')
	else:
		keychain.set_password('Project Oxford', 'Computer Vision API', api_key)

if appex.is_running_extension():
	image = appex.get_image()
else:
	image = photos.capture_image()
	
if image == None:
	image = photos.pick_image(original=True)
	if image == None:
		raise Exception('You must select one image')

enhancerColor = ImageEnhance.Color(image)
image = enhancerColor.enhance(0.0)

output = StringIO.StringIO()
image.save(output, format="PNG")
data = output.getvalue()

# If image size in bytes is larger than +- 4mb
if len(data) > 4000000:
	
	sizes = image.size
	image = image.resize((sizes[0] / 2, sizes[1] / 2))
	output = StringIO.StringIO()
	image.save(output, format='PNG')
	data = output.getvalue()

lang = "unk"
url = "https://api.projectoxford.ai/vision/v1/ocr"

params = {
	"language": lang,
	"detectOrientation": "true"
}

headers = {
	"Content-Type": "application/octet-stream",
	"Ocp-Apim-Subscription-Key": api_key
}

image.show()
console.show_activity()
print('Starting request to Project Oxford...')

r = requests.post(url, data=data, headers=headers, params=params)

console.hide_activity()

if r.status_code == 200:
	print('Request to Project Oxford was successful, building string...')
	
	def words(w):
		return w["text"]
	
	res = json.loads(r.text)
	
	if len(res["regions"]) <= 0:
		raise Exception('No text found in the image')

	txt = "\n".join([[" ".join(map(words, w["words"])) for w in line] for line in [region["lines"] for region in res["regions"]]][0]).encode("utf-8")
	console.hide_output()
	
	if appex.is_running_extension():
		import clipboard
		import console
		clipboard.set(txt)
		console.hud_alert("OCR'd text added to your clipboard")
	else:
		import webbrowser
		from urllib import quote
		url = "interact://x-callback-url/scratchpad?text=" + quote(txt)
		webbrowser.open(url)
elif r.status_code == 401 and console.alert('Bad Subscription Key', 'You got a bad subscription key in the iCloud Keychain, do you wanna change it?', 'Change it') == 1:
	keychain.set_password('Project Oxford', 'Computer Vision API', console.input_alert('Insert your API key', '', api_key))	
else:
	raise Exception('Request returned status code ' + str(r.status_code) + ' and text "' + json.loads(r.text)['message'] + '"')
