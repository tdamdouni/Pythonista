#!/usr/bin/env python

# https://github.com/paultopia/spideyscrape

from bs4 import BeautifulSoup as BS
try:
  from urllib.request import urlopen
except ImportError:
  from urllib import urlopen
import sys, datetime as dt

def clearJunk(BSobj):
  [s.extract() for s in BSobj(['style', 'script'])]

def makeSoup(url):
  soup = BS(urlopen(url))
  clearJunk(soup)
  return soup
  
def getBody(BSobj):
  return ' '.join([str(i) for i in BSobj.find('body').find_all(recursive=False)])
  
def stripAnchor(url):
  return url.partition('#')[0]

def getPage(url):
  soup = makeSoup(url)
  if url.rpartition('.')[2] in ('html', 'htm'):
    url = url[:url.rfind('/') + 1]
  return (soup, url)

def rootify(url):
  protocol, colon_slash_slash, chopped = url.partition('://')
  if protocol in ('http', 'https'):
    base = protocol + colon_slash_slash
  else: 
    base = 'http://'
    chopped = url
  if chopped.find('/') != -1:
    root = chopped[:chopped.find('/')]
  else:
    root = chopped
  return (base, root)

def filterLinks(root, link):
  # checks non-relative links to see if link contains domain of original page
  if link.startswith('http://') or link.startswith('https://'):
    return root in link
  return True 

def transformLink(base, root, url, link):
  if link.startswith('http'):
    return link
  return base + root + link if link[0] == '/' else url + link

def makeLinks(base, root, url, soup):
  links = list(filter(lambda x: 'mailto:' not in x, [stripAnchor(alink['href']) for alink in soup.find_all('a', href=True)]))
  partials = list(filter(lambda x: filterLinks(root, x), [s for (i,s) in enumerate(links) if s not in links[0:i]]))
  return [transformLink(base, root, url, x) for x in partials if x] 

def makeTexts(uniques, soup):
  texts = [getBody(makeSoup(aurl)) for aurl in uniques]
  texts.insert(0, getBody(soup))
  boilerplate = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head><body>'
  return '{}{}</html></body>'.format(boilerplate, '<br><br>'.join(texts))

def savePage(texts):
  filename = 'scrape{:%Y%m%d%H%M%S}.html'.format(dt.datetime.now())
  with open(filename, 'w') as outfile:
    outfile.write(texts)
  return filename

def scrape(start):
  soup, url = getPage(start)
  base, root = rootify(url)
  uniques = makeLinks(base, root, url, soup)
  return makeTexts(uniques, soup)

if __name__ == "__main__":
  args = sys.argv[1:]  # see if the user gave us a command line argument
  try:
    input = raw_input
  except NameError:
    pass
  start = args[0] if args else input('URL to crawl: ')
  html = scrape(start)
  filename = savePage(html)
  print ('Scraping complete! Output saved as: ' + filename)
