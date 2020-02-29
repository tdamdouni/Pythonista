# coding: utf-8

# https://forum.omz-software.com/topic/2022/a-copy-code-button-here-in-the-forum/4

from __future__ import print_function
import clipboard

use_appex = False
try:
	# appex is only available in 1.6 beta, fail gracefully when running in 1.5
	import appex
	use_appex = appex.is_running_extension()
except:
	pass
	
def main():
	if use_appex:
		url = appex.get_url()
	else:
		url = clipboard.get()
	if 'forum.omz-software' not in url:
		print('No forum URL')
		return
	import requests
	import bs4
	html = requests.get(url).text
	soup = bs4.BeautifulSoup(html)
	pre_tags = soup.find_all('pre')
	if pre_tags:
		text = ('\n#%s\n\n' % ('=' * 30)).join([p.get_text() for p in pre_tags])
		clipboard.set(text)
		print('Code copied (%i lines)' % (len(text.splitlines())))
	else:
		print('No code found')
		
if __name__ == '__main__':
	main()

