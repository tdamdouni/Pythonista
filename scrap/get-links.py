from __future__ import print_function
# get_links.py

# https://pythonadventures.wordpress.com/2011/03/10/extract-all-links-from-a-web-page/

import re
import sys
import urllib
import urlparse
from bs4 import BeautifulSoup
import clipboard

class MyOpener(urllib.FancyURLopener):
	version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'
	
def process(url):
	myopener = MyOpener()
	#page = urllib.urlopen(url)
	page = myopener.open(url)
	
	text = page.read()
	page.close()
	
	soup = BeautifulSoup(text)
	for tag in soup.findAll('a', href=True):
		tag['href'] = urlparse.urljoin(url, tag['href'])
		print(tag['href'])
# process(url)

def main():
	clipText = clipboard.get()
	print(clipText)
	process(clipText)
# main()

if __name__ == "__main__":
	main()

