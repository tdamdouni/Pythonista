# coding: utf-8

# https://forum.omz-software.com/topic/3074/send-url-from-extension-to-editorial-app

from __future__ import print_function
import appex
import requests
import webbrowser
import clipboard
import console

from objc_util import *

app=UIApplication.sharedApplication()
url=nsurl('editorial://')
app._openURL_(url)

def main():
	if not appex.is_running_extension():
		url = "www.example.com"
	else:
		url = appex.get_url()
		
if url:
	clipboard.set(url)
# Editorial.app will use the clipboard and paste it at the end of a document
	webbrowser.open('editorial://x-callback-url/open/path-to-file.txt?root=dropbox&command=PasteLink&x-success=pythonista://')
else:
	print('No input URL found.')
	
if __name__ == '__main__':
	main()

