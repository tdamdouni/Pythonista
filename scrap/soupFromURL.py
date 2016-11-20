#!/usr/bin/env python
# create a BeautifulSoup by reading in a webpage
# Current varsion at https://gist.github.com/cclauss/6648735
# usage:
# from soupFromURL import soupFromURL
# theSoup = soupFromURL('http://www.python.org')

import bs4
useRequests = False  # "Python HTTP: When in doubt, or when
try:                 #  not in doubt, use Requests. Beautiful,
	import requests  #  simple, Pythonic." -- Kenny Meyers
	useRequests = True
except:
	from contextlib import closing
	from urllib2 import urlopen
	
def soupFromURL(inURL):
	if useRequests:
		return bs4.BeautifulSoup(requests.get(inURL).text)
	else:
		with closing(urlopen(inURL)) as webPageSource:
			#print('Successfully opened URL: ' + inURL)
			return bs4.BeautifulSoup(webPageSource.read())
			
if __name__ == '__main__':
	theURL = 'http://www.python.org'
	theSoup = soupFromURL(theURL)
	print(theSoup.prettify())

