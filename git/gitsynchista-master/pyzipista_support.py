# coding: utf-8
# This file is part of https://github.com/marcus67/gitsynchista

import os
import sys
global pyzipista_found

_pyzipista_found = False

PYZIPISTA_PATH = '../pyzipista'

path = os.path.abspath(PYZIPISTA_PATH)
print 'checking ', path
if os.path.exists(path):
  if not PYZIPISTA_PATH in sys.path:
    # see http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    sys.path.append(PYZIPISTA_PATH)
    import pyzipista  
    reload(pyzipista)
  _pyzipista_found = True
  
def pyzipista_found():
  return _pyzipista_found
  
def find_config(base_path):
  
  config_file = None
  for rel_path in pyzipista.CONFIG_FILE_SEARCH_PATH:
    filename = os.path.join(base_path, rel_path, pyzipista.PYZIPISTA_CONFIG_FILE)
    if os.path.exists(filename):
      config_file = filename
      break
  
  return config_file


def load_config_file_and_check_zip_required(config_filename):
  return pyzipista.load_config_file_and_check_zip_required(config_filename)
  

def load_config_file_and_zip(config_filename):
  pyzipista.load_config_file_and_zip(config_filename)
  
  
def test():
  print pyzipista_found()
  
if __name__ == '__main__':
  test()