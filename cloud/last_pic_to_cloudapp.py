import photos
import requests
import keychain
from collections import OrderedDict
import console
import StringIO
import webbrowser
import clipboard
import bitly
import datetime

def get_extension():
	ext = 'jpg'
	photo_meta = photos.get_metadata(-1).keys()
	if '{PNG}' in photo_meta:
		ext = 'png'
	elif '{GIF}' in photo_meta:
		ext = 'gif'
	elif '{TIFF}' and '{Exif}' in photo_meta:
		ext = 'jpg'
	return ext
	
last_pic = photos.get_image(-1)
extension = get_extension()

base = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
filename = base + '.' + extension

pic_read = StringIO.StringIO()
last_pic.save(pic_read, extension)

USER = 'n8henrie@gmail.com'
PASS = keychain.get_password('cloudapp', USER)

API_URL = 'http://my.cl.ly/items/new'

s = requests.Session()
s.auth = requests.auth.HTTPDigestAuth(USER, PASS)
s.headers.update({'Accept': 'application/json'})

upload_request = s.get(API_URL).json
if upload_request['uploads_remaining'] > 0:
	url = upload_request['url']
	data = OrderedDict(upload_request['params'])
	
	data['key'] = data['key'].replace(r'${filename}', filename)
	files = {'file': (filename, pic_read.getvalue()) }
	
	stuff = requests.post(url, data=data, files=files, allow_redirects=False)
	
	cloud_url = s.get(stuff.headers['Location']).json['remote_url']
	
	short_url = bitly.shorten_url(cloud_url)
	
	clipboard.set(short_url)
	webbrowser.open('safari-' + short_url)
	
else:
	print('Out of uploads!')
	exit(1)

