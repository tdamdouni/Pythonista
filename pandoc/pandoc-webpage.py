#! /usr/bin/env python2
# -*- coding: utf-8 -*-

# https://gist.github.com/wcaleb/3976662

# pandoc-webpage.py
# Requires: pyandoc http://pypi.python.org/pypi/pyandoc/
# (Change path to pandoc binary in core.py before installing package)
# TODO: Preserve span formatting from original webpage

import urllib2
import pandoc
from bs4 import BeautifulSoup

# Get URLs for the desired webpages from a text file.
urls = open("urls.txt", "r").read()
urls = urls.splitlines()

# Loop through the URLs, converting each page to markdown.
for url in urls:

	response = urllib2.urlopen(url)
	webContent = response.read()
	
	# Prepare the downloaded webContent for parsing with Beautiful Soup
	soup = BeautifulSoup(webContent)
	
	# Get the title of the post
	rawTitle = soup.h2
	title = str(rawTitle)
	
	# Get the date from the post
	rawDate = "Originally posted on " + soup.h3.string
	date = str(rawDate)
	
	# Get rid of the byline div in the post
	byline = soup.find("div", class_="byline")
	byline.decompose()
	
	# Identify the blogPost section, which should now lack the byline
	rawPost = soup.find("div", class_="blogPost")
	
	# Had a lot of problems until I converted rawPost into string, which makes UTF-8
	post = str(rawPost)
	
	# Combine the title and the post body
	fulltext = title + date + post
	
	# Call on pandoc to convert fulltext to markdown and write to file
	doc = pandoc.Document()
	doc.html = fulltext
	webConverted = doc.markdown
	
	# Write to file, getting rid of any literal linebreaks
	f = open('calebpost.txt','a').write(webConverted.replace("\\\n","\n"))

