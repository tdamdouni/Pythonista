# @Drafts
# http://myword.jeffreykishner.com/users/kishner/essays/030.html
# https://gist.github.com/jkishner/28f539d04d2e32c755d2

import requests
import json
import sys
import urllib
import webbrowser
url = sys.argv[1]
data = requests.request('GET','http://api.instagram.com/publicapi/oembed/?url=' + url)
if data.status_code == 200:
	embed = json.loads(data.text)
	img = embed['thumbnail_url']
	img2 = urllib.quote(img, '')
	mid = 'instagram://media?id=' + embed['media_id']	
	mid2 = urllib.quote(mid, '')
	webbrowser.open('drafts4://x-callback-url/create?text=' + img2 + '%0A%0A' + mid2)