import requests
import webbrowser
import re
from bs4 import BeautifulSoup

page = requests.get('http://xkcd.com')
soup = BeautifulSoup(page.text)

comic = soup.find(id='comic').img['src']

page = requests.get('http://xkcd.com')

comic = re.search("http://imgs.xkcd.com/comics/[^\.]*.png",page.text).group()

#alt = re.search('src="http://imgs.xkcd.com/comics/[^\.]*.png"\s*title="([^"]*)"\s*alt=',page.text).groups()[0]

webbrowser.open(comic)

