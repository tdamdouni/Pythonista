'''
Everrista: create Evernote notes with Readability and Pythonista.
'''
from __future__ import print_function

__author__ = 'Serge Boyko aka mcsquaredjr'
__version__ = '0.2.1'
__email__ = "serge dot boyko at gmail dot com"

# Everrista is a script written for Pythonista to create
# Evernote notes from a URL or a text copied in the clipboard with as
# few clicks as possible. Everrista uses Readability Parser API to 
# create clean, nice-looking and easy to read notes.
#
# Before using the script you need to obtain valid Readability and 
# Evernote API tokens. 
#
# Grab Readability API keys from: 
#
# http://www.readability.com/developers/api
#
# Grab Evernote Cloud API token from:
#
# https://www.evernote.com/api/DeveloperToken.action
#
# # Dependencies: 
#
# To convert HTML into ENLM  (the markup used by Evernote, see: 
# http://dev.evernote.com/start/core/enml.php) which permitts a limited
# subset of XHTML tags, Everrista uses the asciinator aka html2text.py 
# that can be downloaded from:
#
# http://www.aaronsw.com/2002/html2text/
#
## Installation: 
#
# 1. Download Everrista gist from: https://gist.github.com/mcsquaredjr/5096503
#
# I recommend to create a folder called everrista and put everrista script
# there.
#
# 2. Use Omz's script to download and install evernote-sdk: 
# https://gist.github.com/omz/5048588
#
# After installing the SDK make sure you add evernote-skd to the sys.path 
# using using something similar to the following line:
#
# sys.path.append('../evernote-sdk')
#
# (It assumes that Everrista script resides inside /everrista folder and the
# SDK is installed inside the evernote-sdk folder; change accordingly if you
# use different layout of folders)
#
# You may find detailed configuration instructions for Evernote SDK installation
# in this thread:
#
# http://omz-software.com/pythonista/forums/discussion/203/using-the-evernote-sdk-in-pythonista#Item_3
#
# 3. Download html2ascii.py from: 
#
# http://www.aaronsw.com/2002/html2text/html2text.py
#
# and put it in the /lib folder of Pythonista. 
#
# # Configuration: 
#
# 1. Replace R_TOKEN and EN_TOKEN values in Everrista with the tokens  obtained 
# from Readability and Evernote sites.
#
# 2. Change the value of BODY_WIDTH variable in html2ascii to 0 if you want to 
# turn wrapping of long lines off (you probably do). By default html2text wraps 
# all lines at position 78.
#
# The MIT License
#
# Copyright (c) 2013 McSquaredJr
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
		 
import sys
# Change the following lines if you use different locations for html2text
# and Evernote SDK
sys.path.append('../lib')
sys.path.append('../evernote-sdk')
import requests
import clipboard
import re
import markdown2
from string import Template
from bs4 import BeautifulSoup   
import cgi                                                                
import html2text
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient

R_SRV_URL = 'https://readability.com/api/content/v1/parser'
# Replace the values below with the values obtained from Readability
# and Evernote dev sites, see notes above
R_TOKEN = 'your readability token'
EN_TOKEN = 'your evernote token'

hdr_tmpl = Template('''\
# $title \n
**Author:** $author \n
**URL:** [$url]($url) \n\n''')

############################################################
#                CLASS READABILITY_REQUEST                 #
############################################################
class Readability_Request(object):
	def __init__(self, token, r_server):
		self.token = token
		self.server = r_server
		
	def make_request(self, url):
		# Get parsed html from readability.com
		pars = dict()
		pars['token'] = self.token
		pars['url'] = url
		r = requests.get(self.server, params=pars)
		title = r.json['title']
		html = r.json['content']
		url = r.json['url']
		author = r.json['author']
		return title, html, url, author, 
		

############################################################
#                  CLASS EVERNOTE_POSTER                   #
############################################################
class Evernote_Poster(object):
	'''Post notes to evernote'''
	
	def __init__(self, token):
		self.token = token
		self.client = EvernoteClient(token=EN_TOKEN, sandbox=False)
		self.user_store = self.client.get_user_store()
		self.note_store = self.client.get_note_store()	

	def check_version(self):
		'''Check for version'''
		version_ok = self.user_store.checkVersion(
			"Version check",
			UserStoreConstants.EDAM_VERSION_MAJOR,
			UserStoreConstants.EDAM_VERSION_MINOR
		)
		if not version_ok:
			return -1
		else: 
			return 0
	
	def _make_note(self, title, content, url):
		'''Prepare a note to be posted'''
		note = Types.Note()
		note.title = title
		# Set up note attributes
		attrs = Types.NoteAttributes()
		attrs.sourceURL = url
		note.attributes = attrs
		note.content = '<?xml version="1.0" encoding="UTF-8"?>'
		note.content += '<!DOCTYPE en-note SYSTEM ' \
			'"http://xml.evernote.com/pub/enml2.dtd">'
		# Wrap content in <en-note>
		note.content += '<en-note>'
		note.content += content
		note.content += '</en-note>'
		return note
	
	def post_note(self, title, note, url):
		'''Post a note to Evernote'''
		ver = self.check_version()
		if ver < 0:
			print('*** VERSION ERROR: Update client to the latest version.')
		else:
			note = self._make_note(title, note, url)
			created_note = self.note_store.createNote(note)	
		return created_note.guid
	
	
############################################################
#                  CLASS CONTENT_CREATOR	           #
############################################################
class Content_Creator(object):
	'''Create note content either from URL or plain text'''
	def __init__(self, clip):
		self.clip = clip	
			
	def make_content(self):
		'''Use Readability parser to get URL content'''
		if self.is_valid_url(self.clip):
			rr = Readability_Request(R_TOKEN, R_SRV_URL)
			title, html, url, author = rr.make_request(self.clip)
			# Create preamble with title and author
			preamble = hdr_tmpl.substitute(title=title, 
			                               author=author, 
			                               url=url)
			txt = preamble + html2text.html2text(html)
			enml = self.html2enml(markdown2.markdown(txt))
		else:
			title = raw_input('Enter note title: ').decode('utf-8')
			url = ''
			# Make sure we escape characthers not allowed in ENML
			enml = self.wrap_in_div(cgi.escape(self.clip))
		# We need to ensure that unicode is processed properly
		return title.encode('utf-8'), enml.encode('utf-8'), url
				
	def is_valid_url(self, url):
		'''Validate URL, return False if not'''
		# Borrowed from Django
		regex = re.compile(
			r'^https?://'  # http:// or https://
			r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
			r'localhost|'  # localhost...
			r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
			r'(?::\d+)?'  # optional port
			r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	   	return url is not None and regex.search(url)

	def html2enml(self, html):
		'''Convert to ENLM and make links look better.'''
		soup = BeautifulSoup(html)
		links = soup.find_all('a')
		for link in links:
			link['style'] = 'text-decoration:none;color:#4682B4;'
			# ENML does not allow html and body
		return soup.body.prettify().replace('body', 'div')
	
	def wrap_in_div(self, txt):
		'''Wrap each line of text in div, required to create plain-text 
		notes in Evernote
		'''
		# wrap each line in <div></div> for ENML
		lines = txt.splitlines()
		wrapped_txt = ''
		for line in lines:
			if line != '':
				wrapped_txt += '<div>' + line + '</div>'
			else:
				wrapped_txt += '<br />'
		return wrapped_txt
			

if __name__ == '__main__':
	# Glue it all together
	clip = clipboard.get()
	cc = Content_Creator(clip)
	title, enml, url = cc.make_content()
	# Make sure we have something to post
	if enml is not None:
		ep = Evernote_Poster(EN_TOKEN)
		guid = ep.post_note(title, enml, url)
		if guid is not None:
			print('=== Success. Posted note with GUID: ', guid)
		else:
			print('*** ERROR: Cannot post to Evernote.')
	else:
		print('*** ERROR: Nothing to post.')
	
	
	
	





