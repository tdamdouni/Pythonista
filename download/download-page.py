# https://gist.github.com/pfcbenjamin/a3c355f6857a00f5b685
import urllib, webbrowser, clipboard, editor, os.path

url = clipboard.get()

page = urllib.urlopen(url)
content = page.read()

# Code below ripped from Ole Zorn's New from Gist script
from urlparse import urlparse
filename = os.path.split(urlparse(url).path)[1]
editor.make_new_file(filename, content)