# https://gist.github.com/m42e/12d4ad4c44dbcfb97f94

#KeychainDB.py
#A script which enables the use of
#the Pythonista keychain as a persistent
#database. The database is accessed like a dict.
#Usage:
#   from keychaindb import KeychainDB
#   kdb = KeychainDB()
#   kdb['key']

#Unfortunately the keychain can only hold
#strings, but it should be easy to type cast

import keychain
from UserDict import DictMixin

DB_NAME = 'KeychainDB'

class KeychainDB (DictMixin):
	def __init__(self, appname, init=None):
		self._keys = []
		self._data = {}
		self._dbname = DB_NAME+appname
		if init is not None:
			for key, value in init:
				self[key] = value
				
	def __setitem__(self, key, value):
		keychain.set_password(self._dbname, key, value)
		
	def __delitem__(self, key):
		for service in keychain.get_services():
			if key in service:
				keychain.delete_password(self._dbname, key)
		#No KeyError because user doesn't want the key there anyway
		
	def __getitem__(self, key):
		for service in keychain.get_services():
			if key == service[1]:
				return keychain.get_password(self._dbname, key)
		raise KeyError
		
	def keys(self):
		return [s[1] for s in keychain.get_services() if s[0] == self._dbname]
		
	def values(self):
		return [keychain.get_password(self._dbname, k) for k in self.keys()]

