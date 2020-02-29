from __future__ import print_function
# https://gist.github.com/paultopia/02ca124a111a70faf174

# This is a very basic scraper-spider for those html books where there's a table of contents page that links to a 
# bunch of sub-pages with actual content (like the documentation for a bunch of libraries).
#
# Dependencies: Beautiful soup 4 on Python 2.7.
# 
# It assumes all content is vanilla html or at least can be accessed through vanilla html.
#
# To use: run script from terminal (etc.), then pass the script a url to the table of contents (ToC)   
# page through the prompt you get. This script scrapes every unique page linked from ToC and 
# concatenates the contents of their html bodies into one big html page (which is technically 
# invalid as lacks html tag, doctype, etc., but every browser in the world forgives this so 
# really who cares?).
# 
# The point is to save those things for offline reading, for planes etc.  It targets pythonista 
# on iPad for optimum usefulness as offline reader, though should also work fine on real 
# computers, also on phones and such.

# This is identical to the functionality of earlier script @ https://gist.github.com/paultopia/460acfda07f9ca7314e5 
# EXCEPT: 
# 1. validates links to make sure they come from same domain as original page 
# 2. handles absolute links
# 3. handles links relative to root (eg starting with '/')

# Please only scrape content with copyright terms that permit copying.  Be nice to writers.  

# The primary intended use of this is to scrape documentation offered to the public under 
# licenses that permit copying, but which are often distributed in clueless formats (such as 
# the documentation for many open-source software packages, which is often provided under 
# Creative Commons or MIT licenses, permitting scraping).

# (c) 2015, Paul Gowder <http://paul-gowder.com>, licensed under the MIT license (see end of file)

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
if url[-5:] == '.html' or url[-4:] == '.htm':
	url = url[:url.rfind('/') + 1]

# a quick bit of link validation follows
if url[:7] == 'http://':
	base = 'http://'
	chopped = url[7:]
elif url[:8] == 'https://':
	base = 'https://'
	chopped = url[8:]
else: 
	base = 'http://'
	chopped = url
if chopped.find('/') != -1:
	root = chopped[:chopped.find('/')]
else: 
	root = chopped

def filterLinks(root, link):
	# checks non-relative links to see if link contains domain of original page
	if link[:7] == 'http://' or link[:8] == 'https://':
		if root not in link:
			return False
	return True 

links = filter(lambda x: 'mailto:' not in x, [stripAnchor(alink['href']) for alink in soup.find_all('a', href=True)])
partials = filter(lambda x: filterLinks(root, x), [s for (i,s) in enumerate(links) if s not in links[0:i]])

def transformLink(base, root, url, link):
	if link [:4] == 'http':
		return link
	if link[0] == '/':
		return base + root + link
	return url + link

uniques = [transformLink(base, root, url, x) for x in partials if x] 

texts = [getBody(makeSoup(aurl)) for aurl in uniques]
texts.insert(0, getBody(soup))
from time import gmtime, strftime
filename = 'scrape' + str(strftime("%Y%m%d%H%M%S", gmtime())) + '.html'
with open(filename, 'w') as outfile:
	outfile.write('<br><br>'.join(texts))

print('Scraping complete! Output saved as: ' + filename)


# The MIT License (MIT)
# Copyright (c) 2015 Paul Gowder <http://paul-gowder.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files 
# (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, 
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do 
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.