# coding: utf-8

# https://www.macstories.net/reviews/pythonista-2-0-brings-action-extension-ipad-pro-support-code-editor-improvements-and-more/

from __future__ import print_function
import httplib, urllib, base64, clipboard, json, requests, datetime, appex, photos, console, dialogs

timestamp = datetime.datetime.now()
name = timestamp.strftime("%Y-%m-%d-%H%M%S") + '.jpeg'

apiKey = ''
apiSecret = ''

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
    final = response['kraked_url']
else:
    print('Fail. Error message: %s ' % response['error'])

urlOcr = '/vision/v1/ocr'

headers = {
    # Request headers
    'User-Agent': 'python',
    'Ocp-Apim-Subscription-Key': '',
}

params2 = urllib.urlencode({
    # Request parameters
    'language': 'en',
    'detectOrientation': 'true',
})

body = {
    "Url": final,
}

print('Performing OCR...')

body = json.dumps(body)

conn = httplib.HTTPSConnection('api.projectoxford.ai')
conn.request("POST", urlOcr, body, headers)
response = conn.getresponse()
back = response.read()
conn.close()

print('OCR successfully performed.')
data = json.loads(back)

s = ''

for item in data["regions"]:
    for line in item["lines"]:
        for word in line["words"]:
            s += ' ' + word["text"]

print(s)
dialogs.share_text(s)
