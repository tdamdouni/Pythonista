#!python2

# https://forum.omz-software.com/topic/3820/how-to-open-a-tab-in-safari-when-already-in-safari

from __future__ import print_function
import clipboard
import webbrowser


def is_url(image_url):
	''' Accepts a url [string]. Returns True if url is valid. '''
	try:
		return image_url.startswith('http://')
	except:
		print('Invalid URL.')
		return False
		
		
def create_url(image_url):
	''' Accepts an image_url [string]. Returns search by image URL. '''
	search_url = 'https://www.google.co.uk/searchbyimage?&image_url='
	try:
		search_url += image_url
	except:
		print('Could not create URL from clipboard.')
	return search_url
	
	
def main():
	image_url = clipboard.get()
	if is_url(image_url):
		search_url = create_url(image_url)
		webbrowser.open('safari-' + search_url)
		print('Done.')
		
if __name__ == '__main__':
	main()

# --------------------

from objc_util import nsurl,UIApplication

app = UIApplication.sharedApplication()
URL = 'https://www.google.co.uk/searchbyimage?&image_url='
app.openURL_(nsurl(URL))

# --------------------

