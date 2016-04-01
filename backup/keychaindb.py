# http://omz-forums.appspot.com/pythonista/post/5878444697059328
# https://gist.github.com/mattparmett/7948268
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
  def __init__(self, init=None):
    self._keys = []
    self._data = {}
    if init is not None:
      for key, value in init:
        self[key] = value

  def __setitem__(self, key, value):
    keychain.set_password(DB_NAME, key, value)

  def __delitem__(self, key):
    for service in keychain.get_services():
      if key in service:
        keychain.delete_password(DB_NAME, key)
    #No KeyError because user doesn't want the key there anyway

  def __getitem__(self, key):
    for service in keychain.get_services():
      if key == service[1]:
        return keychain.get_password(DB_NAME, key)
    raise KeyError

  def keys(self):
    return [s[1] for s in keychain.get_services() if s[0] == DB_NAME]

  def values(self):
    return [keychain.get_password(DB_NAME, k) for k in self.keys()]