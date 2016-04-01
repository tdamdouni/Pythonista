# coding: utf-8
# This file is part of https://github.com/marcus67/gitsynchista

import keychain
import console

def get_password_from_keychain(service, account, message=None):
  ''' Retrieve the working copy key or prompt for a new one. See https://github.com/ahenry91/wc_sync
  '''
  
  if not message:
    message = "Enter password for account '%s' of service '%s'" % (account, service)
  key = keychain.get_password(service, account)
  if not key:
    try:
      key = console.password_alert(message)
    except KeyboardInterrupt as k:
      key = None
    
    if key:
      keychain.set_password(service, account, key)
    else:
      keychain.delete_password(service, account)
  return key  
  