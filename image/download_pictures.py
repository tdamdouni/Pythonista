from __future__ import print_function
# https://github.com/humberry/bs4_examples

from bs4 import BeautifulSoup
import urllib2, os, requests, urlparse

path = os.getcwd() + '/images'
if not os.path.exists(path):
  print('Create new path /images')
  os.mkdir(path)

homepage = urllib2.urlopen('http://imdb.com').read()
soup = BeautifulSoup(homepage)

images = soup.find_all('img')
for image in images:
  url = image['src']
  filename = os.path.basename(urlparse.urlsplit(url)[2])
  dl = requests.get(url, stream=True)
  with open(path + '/' + filename, 'wb') as f:
    for chunk in dl.iter_content(chunk_size=1024):
      if chunk:
        f.write(chunk)
        f.flush()

print('Pictures downloaded to /images')
