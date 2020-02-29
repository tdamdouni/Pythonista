from __future__ import print_function
# https://forum.omz-software.com/topic/795/sharing-code-on-github/29

# https://gist.github.com/michaeluhl/4043334

import base64
import console
import editor
import json
import keychain
import os.path
import pickle
import re
import urllib2

#Perform authorization
def auth(username, password):
    data='{"scopes":["gist"],"note":"gistcheck"}'
    request = urllib2.Request("https://api.github.com/authorizations",data)
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
	db = {}
	if os.path.exists('gistcheck.db'):
		dbfile = open('gistcheck.db','r')
		db = pickle.load(dbfile)
		dbfile.close()
	db[fname]=gist
	dbfile=open('gistcheck.db','w')
	pickle.dump(db,dbfile)
	dbfile.close()

#load a file from a gist		
def load(gist, fname):
	request = urllib2.Request("https://api.github.com/gists/%s" % gist)
	try:
		result = urllib2.urlopen(request)
		rdata = json.loads(result.read())
		result.close()
		url = rdata['files'][fname]['raw_url']
		result = urllib2.urlopen(url)
		rdata = result.read()
		result.close()
		return rdata
	except Exception as e:
		print(e)
	return None

def pull():
	gist = get_gist_id(editor.get_path())
	if gist is not None:
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
		m = m= console.input_alert('Edit Description','Enter a new description:','')
		if m == '': m = None
		return edit(gist,{fname:editor.get_text()},token,m)

def set():
	gist = get_gist_id(editor.get_path())
	if gist == None: gist = ''
	gist = console.input_alert('Assign Gist ID','Enter the gist id for this file',gist)
	set_gist_id(editor.get_path(),gist)

def setup():
	if not os.path.exists('gistcheck_commit.py'):
		f = open('gistcheck_commit.py','w')
		f.writelines(['import gistcheck\n','gistcheck.commit()'])
		f.close()
	if not os.path.exists('gistcheck_pull.py'):
		f = open('gistcheck_pull.py','w')
		f.writelines(['import gistcheck\n','gistcheck.pull()'])
		f.close()
	if not os.path.exists('gistcheck_set.py'):
		f = open('gistcheck_set.py','w')
		f.writelines(['import gistcheck\n','gistcheck.set()'])
		f.close()

if __name__ == '__main__':
	setup()