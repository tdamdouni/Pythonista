# coding: utf-8

# wrapper for pythonista on iOS to scrape a document, pop up 
# an open in dialogue, allow you to do something with it, 
# then delete the original from pythonista 
# sandboxed internal filesystem to avoid clutter.

# use with bookmarklet: 
#
# javascript:window.location='pythonista://scrapewrap.py?action=run&args='+window.location.href;
#
# or use as app extension with new pythonista 2.0 feature

import spideyscrape
import console
import os

# see if called from 2.0 as app extension
url = None
try:
	import appex 
	url = appex.get_url()  
except ImportError:
	pass
if not url:
	import sys
	url =  sys.argv[1]

html = spideyscrape.scrape(url)
filename = spideyscrape.savePage(html)
console.open_in(filename)
os.remove(filename)