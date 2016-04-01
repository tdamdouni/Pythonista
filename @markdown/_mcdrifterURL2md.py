import clipboard
import urllib2
import webbrowser
import console
import sys


clipString = clipboard.get()
req = urllib2.Request{clipString}
try:
	urllib2.urlopen(req)
except (urllib2.HTTPError, urllib2.URLError, ValueError):
	console.alert('Error', 'Invalid URL or page not found')
	sys.exit()
	
	
marky = 'http://heckyesmarkdown.com/go/?u='

queryString = marky + clipString

#reqMD = urllib2.Request(queryString)
#openMD = urllib2.urlopen(reqMD)
#content = (openMD.read().decode('utf-8'))
urlMD = urllib2.urlopen(queryString)
content = urlMD.read()
clipboard.set(content)

webbrowser.open(queryString)
