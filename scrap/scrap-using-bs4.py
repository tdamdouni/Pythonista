# coding: utf-8

# https://forum.omz-software.com/topic/3179/capture-specific-webpage-text-using-regex-searchhtml-and-save-as-new-textile/2

from __future__ import print_function
import requests
from bs4 import BeautifulSoup

url = 'http://www.cheese.com'

soup = BeautifulSoup(requests.get(url).text)

print(soup.find('div', id='abstract')) #find one div with id 'abstract' and print
