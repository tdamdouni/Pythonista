#!python2

# https://www.kochi-coders.com/2011/05/30/lets-scrape-the-page-using-python-beautifulsoup/2/

from __future__ import print_function
from bs4 import BeautifulSoup
import urllib2
import console

url="http://www.utexas.edu/world/univ/alpha/"

page=urllib2.urlopen(url)
soup = BeautifulSoup(page.read())
universities=soup.findAll('a',{'class':'institution'})
for eachuniversity in universities:
	print(eachuniversity['href']+","+eachuniversity.string)

