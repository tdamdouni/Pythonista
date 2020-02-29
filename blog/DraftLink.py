#!python2
# coding: utf-8

# Draft a markdown blog file
# from a this bookmarklet:
# javascript:(function()%7Bif(document.location.href.indexOf('http')===0)document.location.href='pythonista://DraftLink?action=run&argv='+document.location.href;%7D)();

from __future__ import print_function
import clipboard
import sys
import re
import console
import codecs
from os import remove
import webbrowser
import urllib
import dropboxlogin

# Convert title to slug
def convert_title(title):
	# Repace non alphanumerics with dashes
	slug = re.sub(r'[\t !"#$%;:&\'()*\-/<=>?@\[\\\]^_`{|},.]+', "-", title).lower()
	# Remove trailing dashes
	while slug.endswith('-'):
		slug = slug[:-1]
	return slug
	
# Create a draft markdown text file
def makefile(slug, url, title):
	f = codecs.open(slug + '.md', 'w', 'utf-8')
	f.write(title + '\n')
	f.write('======\n')
	f.write('Link: '  + url + '\n')
	f.write('publish-not-yet\n\n')
	isLink = console.alert('', '', 'Blockquote', 'No Blockquote')
	if isLink == 1:
		f.write('> ' + clipboard.get())
	f.close()
	
# Upload draft to Dropbox
def upload(slug, dropbox_draft_path):
	print('\nUploading ' + slug +'.md')
	f = open(slug + '.md')
	db = dropboxlogin.get_client()
	response = db.put_file(dropbox_draft_path + slug + '.md', f)
	remove(slug + '.md')
	
	
if __name__ == '__main__':
	# Path to drafts folder
	dropbox_draft_path = '/Blog/blog/drafts/'
	
	print(sys.argv[1])
	url = sys.argv[1]
	title = sys.argv[2]
	title = console.input_alert('Edit Title', '', title)
	slug = console.input_alert('Edit Slug', '', convert_title(title))
	makefile(slug, url, title)
	upload(slug, dropbox_draft_path)
	
	# Open draft in Nebulous Notes
	nebulous = 'nebulous:/' + dropbox_draft_path + slug + '.md'
	webbrowser.open(nebulous)

