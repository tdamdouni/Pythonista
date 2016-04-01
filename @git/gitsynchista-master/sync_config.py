# coding: utf-8
# This file is part of https://github.com/marcus67/gitsynchista

import config
import client

reload(config)
reload(client)

PASSWORD_USE_KEY_CHAIN = 'USE_KEY_CHAIN'

class WebDavConfig(config.BaseConfig):
  
  def __init__(self):
    
    self.server = 'localhost'
    self.port = 8080
    self.auth_mode = client.AUTH_MODE_DIGEST
    self.username = None
    self.password = PASSWORD_USE_KEY_CHAIN
    self.epoch_delta = 3600
    
  def getIntAttributes(self):
    return ('port', 'epoch_delta')


class RepositoryConfig(config.BaseConfig):

  def __init__(self):
    
    self.name = None
    self.local_path = None
    self.remote_path = None
    self.transfer_to_remote = True
    self.transfer_to_local = True
    self.auto_scan = False
    self.auto_open_app = None
    self.working_copy_wakeup = False

  def getBooleanAttributes(self):
    return ('transfer_to_remote', 'transfer_to_local', 'auto_scan', 'working_copy_wakeup')
          
class SyncConfig(config.BaseConfig):
  
  def __init__(self):
    self.webdav = WebDavConfig()
    self.repository = RepositoryConfig()  