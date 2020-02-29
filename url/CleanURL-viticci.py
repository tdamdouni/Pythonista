from __future__ import print_function
# https://gist.github.com/viticci/8586671
import re
import string
import console
import urllib
import sys
import clipboard
import webbrowser

console.clear()

# Count arguments passed to script, if less than 2 run regex against clipboard
numArgs = len(sys.argv)

if numArgs == 2:
	redirect = sys.argv[1]
elif numArgs < 2:
	redirect = clipboard.get()
	
# Provided by Peter Hansen on StackOverflow:
# http://stackoverflow.com/questions/1986059/grubers-url-regular-expression-in-python/1986151#1986151
pat = r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^%s\s]|/)))'
pat = pat % re.escape(string.punctuation)


match = re.findall(pat, redirect)

if match:
	for x in match:
		console.show_activity()
		# Get the first match without redirects
		cleaned = urllib.urlopen(x[0]).geturl()
		# Get direct image link
		cleaned = cleaned.replace('www.dropbox.com', 'dl.dropboxusercontent.com')
		title = console.input_alert('Image text', 'Type the image alt text below.')
		final = '![' + title + '](' + cleaned + ')'
		clipboard.set(final)
		print('Done.')
elif not match:
	console.alert('No match found')

