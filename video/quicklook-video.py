# coding: utf-8

# https://forum.omz-software.com/topic/3626/play-video-on-ios-quick-look/3

import appex
import console, clipboard
import requests

def download_file(url):
	local_filename = url.split('/')[-1]
	if not local_filename:
		local_filename = 'tmpfile.dat'
	with open(local_filename, 'wb') as f:
		r = requests.get(url, stream=True)
		total_length = r.headers.get('content-length')
		if not total_length:
			f.write(r.content)
		else:
			dl = 0
			total_length = float(total_length)
			for chunk in r.iter_content(1024):
				dl += len(chunk)
				f.write(chunk)
	return local_filename
	
def main():
	if not appex.is_running_extension():
		print('This script is intended to be run from the sharing extension.')
		return
	url = appex.get_url()
	if not url:
		url = clipboard.get()
	console.hud_alert('url: ' + url)
	local_filename = download_file(url)
	console.hud_alert('copying to ' + local_filename)
	console.quicklook(local_filename)
	
if __name__ == '__main__':
	main()

