from __future__ import print_function
# https://gist.github.com/omz/5596891

# Simple URL shortener using is.gd
# 
# Save this script as 'ShortURL' in Pythonista and add the
# bookmarklet below to Safari. The result is copied to the clipboard.

# Bookmarklet:
# javascript:window.location.href='pythonista://ShortURL?action=run&argv='+encodeURIComponent(window.location.href);

import clipboard
import re
import sys

long_url = sys.argv[1]
if long_url is not None and re.match('http(s)?://.*', long_url):
	import urllib
	short_url = urllib.urlopen('http://is.gd/create.php?format=simple&url=' + urllib.quote(long_url, '')).read()
	if re.match('http://is.gd.*', short_url):
		clipboard.set(short_url)
		import webbrowser
		webbrowser.open('safari-' + long_url)
	else:
		print('Error:', short_url)
else:
	print('Invalid/missing URL argument.')