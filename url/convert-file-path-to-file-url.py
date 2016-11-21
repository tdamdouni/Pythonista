# coding: utf-8

# https://forum.omz-software.com/topic/2981/pdf-to-image-conversion/9

# http://stackoverflow.com/questions/11687478/convert-a-filename-to-a-file-url/14298190#14298190

# You can load local files in a web view using a file:// URL. Here's a snippet for converting from a file path to a file URL

import urlparse, urllib

def path2url(path):
	return urlparse.urljoin(
	'file:', urllib.pathname2url(path))

