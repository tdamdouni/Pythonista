import config
import logging
import sync_config

reload(config)
reload(sync_config)

logger = logging.getLogger('gitsynchista')  
logger.setLevel(logging.DEBUG)
logger.handlers = []
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def test():
  
  config_handler = config.ConfigHandler(sync_config.SyncConfig())
  
  sample_config = config_handler.read_config_file('etc/gitsynchista_config_sample')
  
  sample_config.dump()
  
if __name__ == '__main__':
  test()

