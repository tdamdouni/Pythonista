# coding: utf-8
import webbrowser
import urllib
import clipboard

base = 'x-icabmobile://x-callback-url/download?url='
url = clipboard.get()
url = urllib.quote(url, safe='')
webbrowser.open(base + url)