# coding: utf-8
from __future__ import print_function
import requests
from bs4 import BeautifulSoup

url = 'http://www.cheese.com/'
soup = BeautifulSoup(requests.get(url).text)

for i in soup.find_all(lambda tag: tag.parent.name == 'body'):
	print(i.text.strip())
	
#gives a lot of junk.

