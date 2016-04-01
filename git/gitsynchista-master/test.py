# coding: utf-8
# This file is part of https://github.com/marcus67/gitsynchista

import log
import config
import sync_config

reload(log)
reload(config)
reload(sync_config)

global logger

logger = log.open_logging()

def test():
  
  global logger
  
  logger.info("Start test")
  config_handler = config.ConfigHandler(sync_config.SyncConfig())
  
  sample_config = config_handler.read_config_file('etc/gitsynchista_config_sample')
  
  sample_config.dump()
  logger.info("End test")
  
if __name__ == '__main__':
  test()