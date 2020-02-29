from __future__ import print_function
from bs4 import BeautifulSoup
import requests

url = raw_input("Enter a website to extract the URL's from: ")
r = requests.get("http://" + url)
data = r.text

soup = BeautifulSoup(data)
for link in soup.findAll('a'):
    print(link.get('href'))
