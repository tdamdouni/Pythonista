'''This script demonstrates how you can convert Markdown documents to HTML and view the results in the built-in browser.'''

import os, tempfile, codecs
import urllib, urlparse
import console, clipboard, webbrowser
from markdown2 import markdown

def main():
	choice = console.alert('Markdown Conversion', 'What would you like to convert?', 'Demo Document', 'Clipboard')
	if choice == 1:
		with open('Demo.md') as f:
			md = f.read()
	else:
		md = clipboard.get()
	html = markdown(md, extras=['smarty-pants'])
	tempdir = tempfile.gettempdir()
	html_path = os.path.join(tempdir, 'md_temp.html')
	with codecs.open('Template.html', 'r', 'utf-8') as f:
		template = f.read()
	html = template.replace('{{CONTENT}}', html)
	with codecs.open(html_path, 'w', 'utf-8') as f:
		f.write(html)
	file_url = urlparse.urljoin('file:', urllib.pathname2url(html_path))
	webbrowser.open(file_url)

if __name__ == '__main__':
	main()