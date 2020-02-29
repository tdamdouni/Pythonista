from __future__ import print_function
# https://forum.omz-software.com/topic/3185/problems-with-script

import appex
import requests
import webbrowser
import clipboard
import console

def main():
	if not appex.is_running_extension():
		url = "www.example.com"
	else:
		url = appex.get_url()
		
		if url:
			clipboard.set(url)
			# Editorial.app will use the clipboard and paste it at the end of a document
			webbrowser.open('editorial://x-callback-url/open/path-to-file.txt?root=dropbox&command=PasteLink&x-success=pythonista3://')
			
		else:
			print('No input URL found.')
			
if __name__ == '__main__':
	main()
	
# --------------------
from objc_util import UIApplication, nsurl
app = UIApplication.sharedApplication()
app.openURL_(nsurl('editorial://...'))

# --------------------

