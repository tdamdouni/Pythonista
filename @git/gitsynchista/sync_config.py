import config

reload(config)

class WebDavConfig(config.BaseConfig):
  
  def __init__(self):
    
    #super(WebDavConfig, self).__init__():
    self.server = 'localhost'
    self.port = 8080
    self.username = None
    self.password = None
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

  def getBooleanAttributes(self):
    return ('transfer_to_remote', 'transfer_to_local')
          
class SyncConfig(config.BaseConfig):
  
  def __init__(self):
    self.webdav = WebDavConfig()
    self.repository = RepositoryConfig()  

