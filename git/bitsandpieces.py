from __future__ import print_function
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
import gistcheck
 
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

gistcheck.commit()