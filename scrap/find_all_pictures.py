from __future__ import print_function
from bs4 import BeautifulSoup
import urllib2
 
#local file
#soup = BeautifulSoup(open("index.html"))
 
#homepage
homepage = urllib2.urlopen('http://imdb.com').read()
soup = BeautifulSoup(homepage)
 
images = soup.find_all('img')
for image in images:
    print(image['src'])
    print()
