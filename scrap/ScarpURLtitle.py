# coding: utf-8
from __future__ import print_function
import urllib
import clipboard
import bs4
import console

link = clipboard.get()

console.show_activity()

soup = bs4.BeautifulSoup(urllib.urlopen(link))
pageTitle = soup.title.string +' '+ link

console.hide_activity()

console.clear()

print(pageTitle)