# coding: utf-8
import console
console.show_activity()
import clipboard
import webbrowser
import urllib
from urllib import urlencode
import bs4
import sys

numArgs = len(sys.argv)

addnew = 'due://x-callback-url/add?title='

addtime = '&secslater='

console.hide_activity()

if numArgs < 2:

	console.show_activity()
	
	url = clipboard.get()
	
	soup = bs4.BeautifulSoup(urllib.urlopen(url))
	newlink = (soup.title.string + ' ' + url).encode('utf-8')
	
	console.hide_activity()
	
else:

	title = sys.argv[1]
	url = sys.argv[2]
	newlink = title + ' ' + url
	
newtask = console.input_alert('What is this?', 'Type your reminder below')

newtime = console.input_alert('When?', '3600 for 1 hour, 1800 for 30 minutes')

console.hide_activity()

text = newtask + ' - ' + newlink

encoded = urllib.quote(text, safe='')

err_handler = '&x-source=Source%20App&x-error=pythonista://&x-success=' + url

openDue = addnew + encoded + addtime + newtime + err_handler

console.clear()

webbrowser.open(openDue)

