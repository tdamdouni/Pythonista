#!python2

# https://gist.github.com/omz/3908817

# Google Search for Pythonista (iOS)
# Searches Google and copies the first result to the clipboard as
# a Markdown link in the form [title](url).
#
# Inspired by Brett Terpstra's SearchLink:
# http://brettterpstra.com/searchlink-automated-markdown-linking-improved/

from __future__ import print_function
import clipboard

def google(terms):
	import requests
	import cgi
	url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&filter=1&rsz=small&q=' + cgi.escape(terms)
	r = requests.get(url, headers={'Referer': 'http://bretterpstra.com'})
	if r.json:
		response_data = r.json.get('responseData', None)
		if response_data:
			result = response_data['results'][0]
			output_url = result['unescapedUrl']
			output_title = result['titleNoFormatting']
			return output_title, output_url
			
if __name__ == '__main__':
	terms = raw_input('Enter search terms:')
	title, url = google(terms)
	print('First Google Result:')
	print('Title:', title)
	print('URL:', url)
	clipboard.set('[' + title + ']' + '(' + url + ')')

