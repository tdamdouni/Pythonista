# http://www.leancrew.com/all-this/2014/08/automatic-shortened-urls-via-google/

import requests
import json
import clipboard

# Build the request.
shortener = "https://www.googleapis.com/urlshortener/v1/url"
longURL = clipboard.get()
headers = {'content-type': 'application/json'}
payload = {'longUrl': longURL}

# Get the shortened URL and put it on the clipboard.
r = requests.post(shortener, headers=headers, data=json.dumps(payload))
clipboard.set(r.json()['id'])
