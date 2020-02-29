from __future__ import print_function
# https://gist.github.com/paultopia/460acfda07f9ca7314e5

# https://forum.omz-software.com/topic/2502/quick-hackish-html-book-documentation-scraper-for-offline-reading

# very basic scraper-spider for those html books where there's a table of contents page that links to a 
# bunch of sub-pages with actual content.  (Like the documentation for a bunch of libraries.) 
# WARNING: has no validation, assumes pages contain relative links and are all on the same site. 
# (this is an easy tweak but I don't have time today)
# also assumes all content is vanilla html or at least can be accessed through vanilla html.
#
# pass ToC page through raw_input.  This script scrapes every unique page linked from ToC and 
# concatenates the contents of their html bodies into one big html page (which is technically 
# invalid as lacks html tag, doctype, etc., but every browser in the world forgives.
# 
# the point is to save those things for offline reading, for planes etc.  targets pythonista 
# on iPad for optimum usefulness as offline reader, though should also work fine on real 
# computers.

from bs4 import BeautifulSoup as BS
import urllib 

def clearJunk(BSobj):
	[s.extract() for s in BSobj(['style', 'script'])]

def makeSoup(url):
	r = urllib.urlopen(url)
	soup = BS(r)
	clearJunk(soup)
	return soup
	
def getBody(BSobj):
	return ' '.join([str(i) for i in BSobj.find('body').find_all(recursive=False)])
	
def stripAnchor(url):
	badness = url.find('#')
	if badness != -1:
		return url[:badness]
	return url
	
url = raw_input('URL to crawl: ')
soup = makeSoup(url)

links = filter(lambda x: 'mailto:' not in x, [url + stripAnchor(alink['href']) for alink in soup.find_all('a', href=True)])
uniques = [s for (i,s) in enumerate(links) if s not in links[0:i]]

texts = [getBody(makeSoup(aurl)) for aurl in uniques]
texts.insert(0, getBody(soup))
from time import gmtime, strftime
filename = 'scrape' + str(strftime("%Y%m%d%H%M%S", gmtime())) + '.html'
with open(filename, 'w') as outfile:
	outfile.write('<br><br>'.join(texts))

print('scraping complete!')