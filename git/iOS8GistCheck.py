from __future__ import print_function
# Source: https://gist.github.com/5212628
#
# All-purpose gist tool for Pythonista.
#
# When run directly, this script sets up four other scripts that call various
# functions within this file. Each of these sub-scripts are meant for use as
# action menu items. They are:
#
#   Set Gist ID.py   - Set the gist id that the current file should be
#                      associated with.
#
#   Download Gist.py - Download the gist from the URL on the clipboard, and
#                      automatically set the association for it (if possible).
#
#   Commit Gist.py   - Commits the currently open file to the associated gist.
#
#   Pull Gist.py     - Replaces the current file with the latest version from
#                      the associated gist.
#   Create Gist.py   - create a new gist with the current file
#
#
# Scripts created on the first run reference back to the original script. It is
# therefore vital that it is named gistcheck.py so that the references work.
#
# Download Gist.py can also be run as a bookmarklet from Mobile Safari (to
# jump from browsing a gist directly to downloading it in Pythonista) by
# creating a bookmark to:
#
#   javascript:(function()%7Bif(document.location.href.indexOf('http')===0)document.location.href='pythonista://GistDownload?action=run&argv='+document.location.href;%7D)();
#
#
# Credits:
#
# Takes script by spencerogden
# https://gist.github.com/4702275
#
# and replaces auth() function with that from Westacular
# https://gist.github.com/4145515
#
# which was itself the inspiration for spencerogden's version
#
# This combines the gist pull/commit/set id scripts from
# https://gist.github.com/4043334
#
# with the bookmarklet-compatible, multi-gist download script
# https://gist.github.com/5f3f2035d8aa46de42ad
#
# (which in turn is based on https://gist.github.com/4036200,
# which is based on https://gist.github.com/b0644f5ed1d94bd32805)

import clipboard
import console
import editor
import json
import keychain
import os
import re
import requests
import shelve
import urllib2

api_url = 'https://api.github.com/gists/'

class GistDownloadError (Exception): pass
class InvalidGistIDError (Exception): pass

def auth(username, password):
	data='{"scopes":["gist"],"note":"gistcheck"}'
	request = urllib2.Request("https://api.github.com/authorizations",data)
	import base64
	enc = base64.standard_b64encode('%s:%s' % (username, password))
	request.add_header("Authorization", "Basic %s" % enc)
	result = urllib2.urlopen(request)
	rdata = result.read()
	result.close()
	print(rdata)
	return json.loads(rdata)
	
#get auth data
def get_token():
	token = keychain.get_password('gistcheck','gistcheck')
	if token is None:
		u, p = console.login_alert('GitHub Login')
		token = auth(u, p)['token']
		keychain.set_password('gistcheck','gistcheck',token)
	return token
	
def commit_or_create(gist, files, token, message=None):
	payload = {"files":{}}
	if message is not None: payload['description'] = message
	for f, c in files.items():
		payload['files'][os.path.basename(f)] = {"content":c}
	headers = {
	'Content-Type':'application/json',
	'Authorization': 'token %s' % token,
	}
	if gist is None:
		payload['public']=True
		# Create a new gist
		r = requests.post(api_url[:-1],
		data=json.dumps(payload),headers=headers).json()
	else:
		# Commit to existing gist
		r = requests.post(api_url + gist,
		data=json.dumps(payload),headers=headers).json()
	return r
	
def fork(gist,token):
	headers = {
	'Content-Type':'application/json',
	'Authorization': 'token %s' % token,
	}
	return requests.post(api_url + gist + '/forks',
	headers=headers).json()
	
def get_gist_id():
	db = shelve.open('gistcheck.db')
	gist_id = db.get(editor.get_path(),None)
	db.close()
	return gist_id
	
def set_gist_id(gist_id):
	gist_id = extract_gist_id(gist_id)
	db = shelve.open('gistcheck.db')
	db[editor.get_path()] = gist_id
	db.close()
	
def del_gist_id():
	db = shelve.open('gistcheck.db')
	fpath = editor.get_path()
	if fpath in db:
		del db[fpath]
	db.close()
	
def extract_gist_id(gist):
	if re.match(r'^([0-9a-f]+)$', gist):
		return gist
	m = re.match(r'^http(s?)://gist.github.com/([^/]+/)?([0-9a-f]*)', gist)
	if m:
		return m.group(3)
	m = re.match(r'^http(s?)://raw.github.com/gist/([0-9a-f]*)', gist)
	if m:
		return m.group(2)
	raise InvalidGistIDError()
	
#load a file from a gist
def pull():
	gist_id = get_gist_id()
	if gist_id is None:
		console.alert('Error', 'There is no gist id set for this file')
	else:
		fname = os.path.basename(editor.get_path())
		gist_data = requests.get(api_url + gist_id).json()
		try:
			newtext = gist_data['files'][fname]['content']
		except:
			console.alert('Pull Error', 'There was a problem with the pull',gist_data)
		if newtext is not None:
			editor.replace_text(0,len(editor.get_text()),newtext)
			
def commit():
	token = get_token()
	fpath = editor.get_path()
	fname = os.path.basename(fpath)
	m = console.input_alert('Edit Description','Enter a new description:','')
	if m == '': m = None
	gist_id = get_gist_id()
	res = commit_or_create(gist_id,{fpath:editor.get_text()},token,m)
	try:
		id = res['id']
	except KeyError:
		if gist_id:
			f = console.alert('Commit Failed',
			'Do you have permission to commit? Would you like to fork?','Fork')
			if f == 1:
				res = fork(gist_id,token)
				try:
					id = res['id']
				except KeyError:
					console.alert('Fork Error', 'There was a problem with the fork')
				else:
					set_gist_id(id)
					res = commit_or_create(id,{fpath:editor.get_text()},token,m)
					try:
						id = res['id']
					except KeyError:
						console.alert('Commit Error',
						'Commit still failed, maybe fork too')
	else:
		if gist_id is None:
			set_gist_id(id)
	print('success!')
	
def gist_set():
	gist = get_gist_id()
	if gist == None: gist = ''
	gist = console.input_alert('Assign Gist ID','Enter the gist id for this file',gist)
	if gist == '':
		del_gist_id()
	else:
		try:
			set_gist_id(gist)
		except InvalidGistIDError:
			console.alert('Invalid Gist ID', 'That does not appear to be a valid gist id')
			
def download_gist(gist_url):
	# Returns a 2-tuple of filename and content
	gist_id = extract_gist_id(gist_url)
	try:
		gist_info = requests.get(api_url + gist_id).json()
		files = gist_info['files']
	except:
		raise GistDownloadError()
	for file_info in files.values():
		lang =  file_info.get('language', None)
		#if lang != 'Python': <= trying to replace this check
		filename = file_info['filename']
		if os.path.splitext(filename)[1] not in ['.py', '.pyui','.txt']:
			continue
		yield file_info['filename'],gist_id,file_info['content']
		
def makefile(filename,content):
	#replacing with direct file write.
	#editor.make_new_file(filename, content)
	f = open(filename, 'w')
	f.write(content)
	f.close()
	editor.open_file(filename)
	
def download(gist_url):
	try:
		for num, (filename, gist_id, content) in enumerate(download_gist(gist_url), start=1):
			if os.path.isfile(filename):
				i = console.alert('File exists', 'A file with the name ' + filename +
				' already exists in your library.',
				'Auto Rename', 'Skip')
				if i == 1:
					makefile(filename, content)
					set_gist_id(gist_id)
			else:
				makefile(filename, content)
				set_gist_id(gist_id)
	except InvalidGistIDError:
		console.alert('No Gist URL','Invalid Gist URL.','OK')
	except GistDownloadError:
		console.alert('Error', 'The Gist could not be downloaded.')
	if not num:
		console.alert('No Python Files', 'This Gist contains no Python files.')
		
def download_from_args(args):
	if len(args) == 2:
		url = args[1]
	else:
		url = clipboard.get()
	download(url)
	
def setup():
	script_map={
	'GistCommit'  :'gistcheck.commit()',
	'GistPull'    :'gistcheck.pull()',
	'GistSetID'  :'gistcheck.gist_set()',
	'GistDownload':'import sys\nif __name__ == "__main__" : gistcheck.download_from_args( sys.argv )'
	}
	for s,c in script_map.items():
		with open(s+'.py','w') as f:
			f.writelines(['import gistcheck\n','%s\n'%c])
			
if __name__ == '__main__':
	setup()

