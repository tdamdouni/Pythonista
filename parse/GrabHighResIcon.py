# Adapted from Brett Terpstra script : http://brettterpstra.com/2013/04/28/instantly-grab-a-high-res-icon-for-any-ios-app/
# Fetches the 1024px version of an OS X app icon. The result is displayed in Pythonista's console, you can tap and hold to save or copy it.
# If you find any bug, you can find me @silouane20 on Twitter.

from PIL import Image
from StringIO import StringIO
import re
import requests
 
def find_icon(terms):
    search_url = 'http://itunes.apple.com/search?term='+ terms +'&entity=macSoftware'
		
	res = requests.get(search_url)
	m = re.search('artworkUrl512":"(.+?)", ', res.text)
	if m:
		found = m.group(1)
		return found
 
def main():
	terms = raw_input("Input app name: ")
	icon_url = find_icon(terms)
		
	if icon_url:
		file = requests.get(icon_url)
		image = Image.open(StringIO(file.content))
		image.show()
	else:
		print "Failed to get iTunes url"
		
		
if __name__ == "__main__":
	main()
