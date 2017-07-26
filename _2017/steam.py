# https://gist.github.com/clamytoe/5a196a71ca29c7735fc22f6c6eb54bd6

# https://twitter.com/mohhinder/status/864628842849329152

import os
import requests
from bs4 import BeautifulSoup

URL = "http://store.steampowered.com/feeds/newreleases.xml"
FILE = 'newreleases.xml'
USE_LOCAL = False


def read_file():
	with open(FILE, 'rb') as f:
		rss = f.readlines()
	data = ''
	for line in rss:
		data += line
	return data
	

def get_rss():
	r = requests.get(URL)
	with open(FILE, 'wb') as f:
		f.write(r.content)
		rss = r.content
	return rss


def parse_it(data):
	soup = BeautifulSoup(data)
	games = soup.find_all('item')
	for game in games:
		title = game.title.text
		link = game.guid.text
		desc = game.description.text
		
		print(clean_it(title))
		print(link)
		print(clean_it(desc) + '\n')


def clean_it(text):
	t = text.replace('<![CDATA[', '')
	t = t.replace(']]>', '')
	t = t.strip()
	return t

def main():
	if USE_LOCAL and os.path.isfile(FILE):
		print('From local:\n')
		data = read_file()
	else:
		print('From Steam:\n')
		data = get_rss()
	
	parse_it(data)
	

if __name__ == "__main__":
	main()

