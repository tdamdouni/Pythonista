from __future__ import print_function
# https://gist.github.com/djbouche/5019580

# Will prompt a URL to grab gist files, it will pre-populate with current clipboard contents.
# You can also just enter the gist ID by itself.
# Will write each file by its filename

import sys
import requests
import os
import console
import clipboard
import json

def codeget(url):
	r = requests.get('https://api.github.com/gists/%s' % os.path.split(url.strip().split(" ")[0])[-1])
	f = json.loads(r.text)
	for x,v in f['files'].iteritems():
		with open(v['filename'],'w') as ip:
			ip.write(v['content'])
			print('Wrote %d chars to %s' % (len(v['content']),v['filename']))

if __name__ == '__main__':
	a = console.input_alert('URL','Enter URL',clipboard.get())
	codeget(a)
