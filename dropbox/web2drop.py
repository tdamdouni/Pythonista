#coding: utf-8
# Original script by Federico Viticci:
# http://omz-software.com/pythonista/forums/discussion/comment/165#Comment_165
# Modified to create Markdown as well using Brett Terpstra's site

# dropboxlogin must be setup prior to using this script
# Script by OMZ located here: https://gist.github.com/4034526

# Run manually using a URL in the clipboard or use a bookmarlet to open from Safari
# javascript:window.location='pythonista://web2drop?action=run&argv='+encodeURIComponent(document.title)+'&argv='+encodeURIComponent(document.location.href);

from __future__ import print_function
import clipboard
import urllib2
import console
from dropboxlogin import get_client
dropbox_client = get_client()
import keychain
import time
import webbrowser
import sys
import urllib
import bs4

numArgs = len(sys.argv)

console.clear()

if numArgs < 2:
	url = clipboard.get()
	console.show_activity()
	
	soup = bs4.BeautifulSoup(urllib.urlopen(url))
	title = soup.title.string
	name = title.encode('utf-8')
	
	console.hide_activity()
	
else:
	webpage = sys.argv[1]
	name = webpage.encode('utf-8')
	url = sys.argv[2]
	
insta = 'http://instapaper.com/text?u='
marky = 'http://heckyesmarkdown.com/go/?read=1&u='

instaURL = insta + url
markURL = marky + url

print('Retrieving reading list file...')
retrieve = dropbox_client.get_file('/Reading/Links.txt')

old = open('Links.txt', 'w')
old.write(retrieve.read())
old.write('\n'+instaURL)
old.close()

new = open ('Links.txt')

print('Updating reading list file...')
response = dropbox_client.put_file('/Reading/Links.txt',new,True)
new.close()

print('Generating Markdown file...')
getText = urllib2.Request(markURL)
openText = urllib2.urlopen(getText)
content = (openText.read().decode('utf-8'))
final = content.encode('utf-8')

md = open('temp.md', 'w')
md.write(final)
md.close()

md = open('temp.md')

#encode = urllib.quote(name, safe='')
print('Uploading Markdown file to Dropbox..')
response = dropbox_client.put_file('/Reading/'+name+'.md',md)
md.close()

print('Complete')

