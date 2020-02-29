from __future__ import print_function
# https://github.com/polymerchm/flashcard

import urllib2, os, os.path, bs4
import re
from shutil import copyfileobj

pth = "http://192.168.1.192:8888/"
response = urllib2.urlopen(pth)
html = response.read()
soup = bs4.BeautifulSoup(html)
for link in soup.find_all('a'):
	dir = link.get('href')
	dir_unesc = urllib2.unquote(dir)
	try:
		os.mkdir('ASL/'+dir_unesc)
		print('created directory for '+dir_unesc)
	except:
		continue
	
	response = urllib2.urlopen(pth+dir)
	html = response.read()
	soup2 = bs4.BeautifulSoup(html)
	for link2 in soup2.find_all('a'):
		file = link2.get('href')
		if (file != '/'):
			file_unesc = urllib2.unquote(file)			
			im = urllib2.urlopen(pth+dir+file)
			with open('ASL/'+dir_unesc +file_unesc, 'wb') as out:
				copyfileobj(im,out)
	
