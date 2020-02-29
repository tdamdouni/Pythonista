from __future__ import print_function
import clipboard
import console
import webbrowser
import string
from glob import glob
from urlparse import urlparse
import sys

twitter_name = 'jayhickey'

try:
	mytext = sys.argv[1]
	print(clipboard.get())
except IndexError:
	mytext = clipboard.get()
	
	
u = urlparse(mytext)
mytext = mytext.replace('https://twitter.com/', 'tweetbot://')
mytext = mytext.replace('statuses', 'status')
mytext = mytext.replace('http://twitter.com/', 'tweetbot://')
mytext = mytext.replace('http://mobile.twitter.com/', 'tweetbot://')
mytext = mytext.replace('https://mobile.twitter.com/', 'tweetbot://')

if mytext.count('/') < 3 or mytext.find('tweets') != -1:
	mytext = 'tweetbot://' + twitter_name + '/user_profile' + u.path
	
# console.clear()
print(mytext)

webbrowser.open(mytext)

