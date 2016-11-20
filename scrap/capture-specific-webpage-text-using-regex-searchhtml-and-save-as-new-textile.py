# https://forum.omz-software.com/topic/3179/capture-specific-webpage-text-using-regex-searchhtml-and-save-as-new-textile

import bs4, requests

def get_soup(url):
	return soup = bs4.BeautifulSoup(requests.get(url).text, 'html5lib')

