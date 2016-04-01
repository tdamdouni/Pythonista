# coding: utf-8

# https://gist.github.com/Gerzer/cce8d1383194d5495298

import appex
import requests

def main():
	if not appex.is_running_extension():
		print 'Running in Pythonista app, using test data...\n'
		url = 'http://example.com'
	else:
		url = appex.get_url()
	if url:
		out_file = open(url.split('/')[-1], 'wb')
		out_file.write(requests.get(url).content)
		out_file.close()
	else:
		print 'No input URL found.'

if __name__ == '__main__':
	main()