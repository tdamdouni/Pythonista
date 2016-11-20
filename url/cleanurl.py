#!/usr/bin/python

# coding: utf-8

# https://gist.github.com/gps/6a118b88bf57f01a483bac69fb61a933

import appex
import clipboard

from urlparse import urlparse, urlunparse, parse_qs
from urllib import urlencode


def get_asin(url):
	'''
	Amazon links can be simplified to have a structure of http://www.amazon.com/gp/product/<ASIN>
	See: http://leancrew.com/all-this/2015/06/clean-amazon-links-with-textexpander/
	
	This function attempts to parse an ASIN from a url, and returns one if found. None otherwise.
	'''
	split = url.split('/')
	for i, part in enumerate(split):
		part = part.strip()
		if 'dp' == part:
			try:
				return split[i + 1]
			except IndexError as e:
				print 'Unable to find ASIN'
				return None
		if 'gp' == part:
			try:
				if split[i + 1].strip() == 'product':
					return split[i + 2]
			except IndexError as e:
				print 'Unable to find ASIN'
				return None
				
				
def should_strip_param(param):
	if param.startswith('utm_'):
		# Google analytics crap
		return True
	if param == 'ncid':
		# Tech crunch rss feed includes this thing
		return True
	return False
	
	
def clean_url(url):
	url = url.lower()
	parsed = urlparse(url)
	
	if 'amazon' in url:
		return urlunparse([
		parsed.scheme,
		parsed.netloc,
		'/gp/product/' + get_asin(url),
		parsed.params,
		urlencode({}, doseq=True),
		parsed.fragment
		])
		
	qd = parse_qs(parsed.query, keep_blank_values=True)
	filtered = dict( (k, v) for k, v in qd.iteritems() if not should_strip_param(k))
	return urlunparse([
	parsed.scheme,
	parsed.netloc,
	parsed.path,
	parsed.params,
	urlencode(filtered, doseq=True),
	parsed.fragment
	])
	
	
def main():
	if not appex.is_running_extension():
		print 'Running in Pythonista app, using test data...\n'
		url = 'https://500px.com/photo/152315787/mankins-by-forrest-mankins?utm_campaign=mankins-by-forrest-mankins&utm_medium=social&utm_source=500px'
	else:
		url = appex.get_url()
	if url:
		cleaned_url = clean_url(url)
		clipboard.set(cleaned_url)
		print 'Original url:', url
		print
		print 'Cleaned url (copied to clipboard):', cleaned_url
	else:
		print 'No input URL found.'
		
if __name__ == '__main__':
	main()

