from __future__ import print_function
# http://www.jackenhack.com/scripting-programming-iphone-ipad-python-pythonista-review/

# coding: utf-8

# A simple script for showing the HTML code of a page directly from mobile Safari.

# add a bookmark in the browser with the JavaScript code:   
# javascript:window.location='pythonista://showHTML?action=run&argv='+encodeURIComponent(document.location.href);  

#  
# _ _   
# | | | |   
# | | __ _ ___| | _____ _ __   
# _ | |/ _` |/ __| |/ / _ \ '_ \   
# | |__| | (_| | (__| < __/ | | |  
# \\____/ \\__,_|\\___|_|\\_\\___|_| |_|

import sys  
import console  
import urllib  
from bs4 import BeautifulSoup

numArgs = len(sys.argv)  
print(numArgs)  
if numArgs != 2:  
	console.alert('This script needs an URL as an argument.')  
else:  
	url = sys.argv[1]  
	usock = urllib.urlopen(url)  
	data = usock.read()  
	usock.close()  
	soup = BeautifulSoup(data)  
	console.clear()  
print(soup.prettify())