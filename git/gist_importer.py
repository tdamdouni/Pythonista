#!python2
# coding: utf-8

# https://gist.github.com/b00giZm/6866497

# Since there's no Git or Dropbox support in Pythonista (yet), here's a little script for importing Python gists into your Pythonista library. Here's how you do it:

# Create a personal access token for your Github account

# Launch Pythonista on your iPad or iPad and open the console

# Run the following code:

#import keychain
#keychain.set_passwort('github', <your_github_username>, <your_access_token>)

# Copy the contents of this gist onto your clipboard and paste it into a new Pythonista script called gist_importer

# Change the values for GITHUB_USER and FOLDER_PREFIX to match your account / setup

# Install the following bookmarklet for your iOS browser of choice

# javascript:window.location='pythonista://gist_importer?action=run&argv='+encodeURIComponent(document.location.href);

# Find yourself a nice Python gist and hit the bookmarklet. Boom.

from __future__ import print_function
import keychain
import requests
import editor
import sys
import re

GITHUB_USER   = 'tdamdouni'
GITHUB_TOKEN  = keychain.get_password('github', GITHUB_USER)
FOLDER_PREFIX = '~/Documents/inbox' # Usage: 'Path/to/folder/'

if len(sys.argv) < 2:
	print('No Gist URL provided')
	sys.exit(1)
	
pattern = re.compile('https://gist.github.com/[a-zA-Z0-9_]+/([a-f0-9]+)')
match = pattern.search(sys.argv[1])
try:
	gist_id = match.group(1)
except IndexError:
	print("Could not parse Gist ID from URL '%s'" % sys.argv[1])
	sys.exit(1)
	
gist_url = 'https://api.github.com/gists/' + gist_id

r = requests.get(gist_url, auth=(GITHUB_USER, GITHUB_TOKEN))
if r.status_code is not 200:
	print("Something's wrong! API returned status %d" % r.status_code)
	sys.exit(1)
	
files = r.json['files']
for key in files.keys():
	tup = key.rpartition('.')
	name = tup[0]
	if name is '':
		name = tup[2]
	if files[key]['language'] == 'Python':
		# Create file
		editor.make_new_file(FOLDER_PREFIX + name, files[key]['content'])
		print("Imported script '%s'" % name)
		
editor.reload_files()

