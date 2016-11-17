# coding: utf-8

# https://forum.omz-software.com/topic/3204/share-code-webviewdatareceiver

import ui
import urllib
from objc_util import *

#a way to 'cheat' and get data from a webview to the script without using a server.
#uses javascript and the webview delegate to deliver data back to the script (kind of like an urlscheme for your script)
#
#this is just a quick sample to show the possibility

class WebViewDataReceiver (ui.View):
	def __init__(self, html, flex='WH'):
		self.w = ui.WebView(flex='WH')
		self.w.delegate = self
		self.w.scales_page_to_fit = False
		self.w.load_html(html)
		self.add_subview(self.w)
		self.present()
		
	def webview_should_start_load(self, webview, url, nav_type):
		#need to filter the url; better to use a kind of urlscheme.
		#recommend starting with something like myscript://
		if url.startswith('myscript://'):
			self.name = urllib.unquote(url.split('myscript://')[1])
			
			#stop the activity indicator; necessary
			UIApplication.sharedApplication().setNetworkActivityIndicatorVisible_(False)
			return False
		else:
			return True
			
if __name__ == '__main__':
	html = '''<a onclick="location.href='myscript://Ha! Click-bait!'">Click here</a>'''
	
	WebViewDataReceiver(html)
	
# --------------------

