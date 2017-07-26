import clipboard
import string
import sys
import webbrowser

try:
	article = sys.argv[1]
except IndexError:
	article = clipboard.get()
	
article = article.replace('http://en.wikipedia.org/wiki/', 'x-articles://wikipedia.org/wiki/')
article = article.replace('https://en.wikipedia.org/wiki/', 'x-articles://wikipedia.org/wiki/')
article = article.replace('http://en.m.wikipedia.org/wiki/', 'x-articles://wikipedia.org/wiki/')
article = article.replace('https://en.m.wikipedia.org/wiki/', 'x-articles://wikipedia.org/wiki/')

webbrowser.open(article)

