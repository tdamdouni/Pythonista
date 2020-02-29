from __future__ import print_function
#Let python know we are going to use the urllib library which handles all of the HTTP protocol and header details. 
import urllib
from bs4 import BeautifulSoup

#Prompt for a web address
url = raw_input('Enter a url - ')

#Opens the web page and read the data 
html = urllib.urlopen(url).read()

#Data is passed to the BeautifulSoup parser
soup = BeautifulSoup(html, "html5lib")

#Retrieve all of the anchor tags 
tags = soup('a')
for tag in tags:
    print(tag)
    #print out the href attribute for each
    print(tag.get('href', None))