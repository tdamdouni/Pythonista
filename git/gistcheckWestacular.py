from __future__ import print_function
# https://forum.omz-software.com/topic/795/sharing-code-on-github/29

# Source: https://gist.github.com/4145515
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
#
# Download Gist.py can also be run as a bookmarklet from Mobile Safari (to
# jump from browsing a gist directly to downloading it in Pythonista) by
# creating a bookmark to:
#
#   javascript:(function()%7Bif(document.location.href.indexOf('http')===0)document.location.href='pythonista://Download%20Gist?action=run&argv='+document.location.href;%7D)();
#
#
# Credits:
#
# This combines the gist pull/commit/set id scripts from
# https://gist.github.com/4043334
#
# with the bookmarklet-compatible, multi-gist download script
# https://gist.github.com/5f3f2035d8aa46de42ad
#
# (which in turn is based on https://gist.github.com/4036200,
# which is based on https://gist.github.com/b0644f5ed1d94bd32805)

import console
import editor
import json
import keychain
import os.path
import pickle
import re
import urllib2

class InvalidGistURLError (Exception): pass
class NoFilesInGistError (Exception): pass
class GistDownloadError (Exception): pass
class InvalidGistIDError (Exception): pass

#Perform authorization
def auth(username, password):
	data='{"scopes":["gist"],"note":"gistcheck"}'
	request = urllib2.Request("https://api.github.com/authorizations",data)
	import base64
	enc = base64.standard_b64encode('%s:%s' % (username, password))
	request.add_header("Authorization", "Basic %s" % enc)   
	result = urllib2.urlopen(request)
	rdata = result.read()
	result.close()
	return rdata
	
def edit(gist, files, token, message=None):
	reqdict = {"files":{}}
	if message is not None: reqdict['description']=message
	for f, c in files.items():
		reqdict['files'][f] = {"content":c}
	request = urllib2.Request("https://api.github.com/gists/%s" % gist,json.dumps(reqdict))
	request.add_header("Authorization", "token %s" % token)
	request.add_header('Content-Type','application/json')
	try:
		result = urllib2.urlopen(request)
		rdata = result.read()
		result.close()
		return rdata
	except Exception as e:
		print(e)
	return None
	
def get_gist_id(fname):
	if os.path.exists('gistcheck.db'):
		dbfile = open('gistcheck.db','r')
		db = pickle.load(dbfile)
		dbfile.close()
		return db.get(fname,None)
	return None
	
def set_gist_id(fname, gist):
	gist = extract_gist_id(gist)
	db = {}
	if os.path.exists('gistcheck.db'):
		dbfile = open('gistcheck.db','r')
		db = pickle.load(dbfile)
		dbfile.close()
	db[fname]=gist
	dbfile=open('gistcheck.db','w')
	pickle.dump(db,dbfile)
	dbfile.close()

def extract_gist_id(gist):
	if re.match(r'^([0-9a-f]+)$', gist):
		return gist
	m = re.match(r'^http(s?)://gist.github.com/([0-9a-f]*)$', gist)
	if m:
		return m.group(2)
	else:
		raise InvalidGistIDError()

#load a file from a gist
def load(gist, fname):
	request = urllib2.Request("https://api.github.com/gists/%s" % gist)
	try:
		result = urllib2.urlopen(request)
		rdata = json.loads(result.read())
		result.close()
		return rdata['files'][fname]['content']
		# url = rdata['files'][fname]['raw_url']
		# result = urllib2.urlopen(url)
		# rdata = result.read()
		# result.close()
		# return rdata
	except Exception as e:
		print(e)
	return None

def pull():
	gist = get_gist_id(editor.get_path())
	if gist is None:
		console.alert('Error', 'There is no gist id set for this file')
	else:
		fname = os.path.basename(editor.get_path())
		newtxt = load(gist,fname)
		if newtxt is not None:
			editor.replace_text(0,len(editor.get_text()),newtxt)

def commit():
	gist = get_gist_id(editor.get_path())
	if gist is not None:
		token = keychain.get_password('gistcheck','gistcheck')
		if token is None:
			u, p = console.login_alert('GitHub Login')
			r = json.loads(auth(u, p))
			print(r)
			token = r['token']
			keychain.set_password('gistcheck','gistcheck',token)
		fname = os.path.basename(editor.get_path())
		m = console.input_alert('Edit Description','Enter a new description:','')
		if m == '': m = None
		return edit(gist,{fname:editor.get_text()},token,m)

def set():
	gist = get_gist_id(editor.get_path())
	if gist == None: gist = ''
	gist = console.input_alert('Assign Gist ID','Enter the gist id for this file',gist)
	try:
		set_gist_id(editor.get_path(),gist)
	except InvalidGistIDError:
		console.alert('Invalid Gist ID', 'That does not appear to be a valid gist id')

def download_gist(gist_url):
	# Returns a 2-tuple of filename and content
	# console.show_activity()
	raw_match = re.match('http(s?)://raw.github.com/gist/', gist_url)
	if raw_match:
		import requests
		from urlparse import urlparse
		filename = os.path.split(urlparse(gist_url).path)[1]
		try:
			r = requests.get(gist_url)
			content = r.text
			yield filename, content
		except:
			raise GistDownloadError()
	else:
		gist_id_match = re.match('http(s?)://gist.github.com/([0-9a-f]*)', gist_url)
		if gist_id_match:
			import requests
			gist_id = gist_id_match.group(2)
			json_url = 'https://api.github.com/gists/' + gist_id
			try:
				import json
				gist_json = requests.get(json_url).text
				gist_info = json.loads(gist_json)
				files = gist_info['files']
			except:
				raise GistDownloadError()
			for file_info in files.values():
				lang =  file_info.get('language', None)
				if lang != 'Python':
					continue 
				filename = file_info['filename']
				content = file_info['content']
				yield filename, content
		else:
			raise InvalidGistURLError()

def download(gist_url):
	num = 0
	try:
		for num, (filename, content) in enumerate(download_gist(gist_url), start=1):
			if os.path.isfile(filename):
				i = console.alert('File exists', 'A file with the name ' + filename + 
								  ' already exists in your library.',
								  'Auto Rename', 'Skip')
				if i == 1:
					editor.make_new_file(filename, content)
			else:
				editor.make_new_file(filename, content)
				try:
					set_gist_id(editor.get_path(), gist_url)
				except InvalidGistIDError:
					# console.alert('Gist ID not set', filename + '\n' + gist_url)
					pass
	except InvalidGistURLError:
		console.alert('No Gist URL',
					  'Invalid Gist URL.',
					  'OK')
	except GistDownloadError:
		console.alert('Error', 'The Gist could not be downloaded.')
	if not num:
		console.alert('No Python Files', 'This Gist contains no Python files.')


def setup():
	if not os.path.exists('Commit Gist.py'):
		f = open('Commit Gist.py','w')
		f.writelines(['import gistcheck\n','gistcheck.commit()\n'])
		f.close()
	if not os.path.exists('Pull Gist.py'):
		f = open('Pull Gist.py','w')
		f.writelines(['import gistcheck\n','gistcheck.pull()\n'])
		f.close()
	if not os.path.exists('Set Gist ID.py'):
		f = open('Set Gist ID.py','w')
		f.writelines(['import gistcheck\n','gistcheck.set()\n'])
		f.close()
	if not os.path.exists('Download Gist.py'):
		f = open('Download Gist.py','w')
		from textwrap import dedent
		f.write(dedent('''\
				import gistcheck
				import clipboard
				if __name__ == '__main__':
					if len(sys.argv) == 2:
						url = sys.argv[1]
					else:
						url = clipboard.get()
					gistcheck.download(url)
				'''))
		f.close()

if __name__ == '__main__':
	setup()