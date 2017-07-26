# https://gist.github.com/viticci/b27acfeb04c25101e4ea

from bs4 import BeautifulSoup
import urllib2
import appex
import dialogs
import clipboard

channel = appex.get_url()
webpage = urllib2.urlopen(channel)
soup = parser(webpage)

feeds = soup.findAll("link", rel="alternate")
for RSS_link in feeds:
	url = RSS_link.get("href", None)
	if 'feeds' in url:
		dialogs.alert('Found Channel RSS', url, 'Copy')
		clipboard.set(url)
