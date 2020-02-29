from __future__ import print_function
# https://forum.omz-software.com/topic/1966/download-script-into-pythonista/25

# python2

import urllib2

url = 'https://raw.githubusercontent.com/humberry/PhoneManager/master/PhoneManager.py'
print(urllib2.urlopen(url).read())

# --------------------

# python3

import urllib.request

url = 'https://raw.githubusercontent.com/humberry/PhoneManager/master/PhoneManager.py'
req = urllib.request.urlopen(url)
print(req.read().decode('utf-8'))

# --------------------

# python

import requests

url = 'https://raw.githubusercontent.com/humberry/PhoneManager/master/PhoneManager.py'
print(requests.get(url).text)

# --------------------
