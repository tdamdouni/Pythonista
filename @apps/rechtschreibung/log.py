import logging
import logging.handlers
import logging.config
import sys
import os
import shutil
import json

import log_stat

LOGGING_FILENAME = "etc/log_config.json"
LOGGING_TEMPLATE_FILENAME = "etc/log_config_template.json"

def open_logging(module_name, reload = False):
  
  global logger
  
  if reload or not log_stat.get_log_started():

    log_stat.set_log_started(True)    
    copy_template = os.path.exists(LOGGING_TEMPLATE_FILENAME) and not os.path.exists(LOGGING_FILENAME)
    if copy_template:
      shutil.copyfile(LOGGING_TEMPLATE_FILENAME, LOGGING_FILENAME)
    logging_config_json_file = open(LOGGING_FILENAME)
    parsed_logging_data = json.load(logging_config_json_file)
    logging.config.dictConfig(parsed_logging_data)

    logger = logging.getLogger('log')
    if copy_template:
      logger.info("Copied logging configuration template %s" % LOGGING_TEMPLATE_FILENAME)
    logger.info("Loaded logging configuration from %s" % LOGGING_FILENAME)  
    logger.info("Starting logging")
    
  return logging.getLogger(module_name)

def test():
  
  logger = open_logging('test', True)
  logger.error("This is an error")
  logger.warning("This is a warning")  
    
if __name__ == '__main__':
  test()
  