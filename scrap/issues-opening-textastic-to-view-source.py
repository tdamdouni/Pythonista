# coding: utf-8

# https://forum.omz-software.com/topic/2660/issues-opening-textastic-to-view-source

from __future__ import print_function
import appex
import webbrowser
from urlparse import urlsplit

def main():
	if not appex.is_running_extension():
		print('This script is intended to be run from the sharing extension.')
		return
	url = appex.get_url()
	if not url:
		print('No input URL found.')
		return
	url = urlsplit(url)
	url = 'textastic://' + url.netloc + url.path + url.query + url.fragment
	print(url)
	webbrowser.open(url)
	
if __name__ == '__main__':
	main()

