# coding: utf-8

# https://gist.github.com/wcaleb/3afca0083063b7f9ab91

import os
from bs4 import BeautifulSoup

files = os.listdir('.')

for file in files:
	html = open(file, 'r').read()
	soup = BeautifulSoup(html)
	url = soup.find(rel='canonical')['href']
	open(url.split('/')[-1] + '.html', 'w').write(html)

