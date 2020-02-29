#!python2
# coding: utf-8

# https://gist.github.com/philgruneich/6859485

# Adapted from Brett Terpstra script: http://brettterpstra.com/2013/04/28/instantly-grab-a-high-res-icon-for-any-ios-app/
# Gets the 1024px version of an app icon and applies a rounded mask. The result is displayed in Pythonista's console, you can tap and hold to save or copy it.
# You may find odd result: try searching for both device categories.
# If you find any bug, you can find me @silouane20 on Twitter.
# iOS 7 masks by @pgruneich on Twitter.

from __future__ import print_function
from PIL import Image
from StringIO import StringIO
import re
import requests

def find_icon(terms, platform):
	if platform == "1":
		search_url = 'http://itunes.apple.com/search?term='+ terms +'&entity=software'
	else:
		search_url = 'http://itunes.apple.com/search?term='+ terms+'&entity=iPadSoftware'
		
	res = requests.get(search_url)
	m = re.search('artworkUrl512":"(.+?)", ', res.text)
	if m:
		found = m.group(1)
		return found
		
def main():
	print("Select chosen platform \n")
	print("[1] iPhone")
	print("[2] iPad\n")
	platform = raw_input("")
	
	if platform == "x":
		print("Exited")
	else:
		terms = raw_input("Input app name: ")
		icon_url = find_icon(terms, platform)
		
		if icon_url:
			file = requests.get(icon_url)
			image = Image.open(StringIO(file.content))
			(width,height) = image.size
			if width == 512:
				mask_url = "https://dl.dropboxusercontent.com/u/100460186/iOS7Mask512.png"
			elif width == 1024:
				mask_url = "https://dl.dropboxusercontent.com/u/100460186/iOS7Mask1024.png"
			else:
				image.show()
				sys.exit()
				
			file = requests.get(mask_url)
			mask = Image.open(StringIO(file.content))
			
			image.paste(mask,(0,0,width,width),mask)
			image.show()
		else:
			print("Failed to get iTunes url")
			
			
if __name__ == "__main__":
	main()

