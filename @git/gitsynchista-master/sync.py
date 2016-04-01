# coding: utf-8
# This file is part of https://github.com/marcus67/gitsynchista

import sys
import client
import os
import time
import datetime
import logging
import re
import tempfile
import StringIO
import requests
import keychain

import log
import config
import sync_config
import util
import url_scheme_support
import working_copy
import pyzipista_support

reload(log)
reload(client)
reload(config)
reload(sync_config)
reload(util)
reload(url_scheme_support)
reload(working_copy)
reload(pyzipista_support)

GIT_IGNORE_FILE = '.gitignore'
GITSYNCHISTA_IGNORE_FILE = 'gitsynchista_ignore'
GITSYNCHISTA_IGNORE_FILE_2 = 'gitsynchista_ignore.txt'
GITSYNCHISTA_CONFIG_FILE = 'gitsynchista_config'

ADDITIONAL_IGNORE_PATTERNS = '.*'

SUPPRESS_PATTERNS = '.git'

global logger

logger = log.open_logging(__name__)

class File(object):
  
  def __init__(self, name, physical_name, base_name, mtime, sub_files = None, is_ignored=False):
    
    self.name = name
    self.physical_name = physical_name
    self.base_name = base_name
    self.mtime = mtime
    self.sub_files = sub_files
    self.is_ignored = is_ignored
    
  def is_directory(self):
    return self.sub_files != None
    
  def __str__(self):
    fmt = "log=%s phys=%s dir=%s ign=%s %s"
    return fmt % (self.name, self.physical_name, self.is_directory(), self.is_ignored, time.ctime(self.mtime))
    
def compare_files_by_name(file1, file2):
  return cmp(file1.name, file2.name)
  
class IgnoreInfo(object):
  
  def __init__(self, file_string):
    
    global logger
    
    if file_string:
      pattern_string = ('^' + file_string.replace('.','\.').replace('*', '.*').replace('\n','$|^') + '$').replace('|^$', '')
      logger.debug("Created IgnoreInfo with pattern regex '%s'" % pattern_string)
      self.regex = re.compile(pattern_string)     
    else:
      self.regex = None   
    
  def is_ignored(self, name):
    return self.regex.match(name) != None if self.regex else False
    
global_ignore_info = IgnoreInfo(ADDITIONAL_IGNORE_PATTERNS)
global_suppress_info = IgnoreInfo(SUPPRESS_PATTERNS)

class FileAccess(object):
  
  def __init__(self, root_path):
    self.root_path = root_path
  
  def load_directory(self, base_path=None, parent_is_ignored=False):
    
    base_path = base_path or self.root_path
    logger.info("Loading file directory '%s'" % base_path)
    files = []
    github_ignore_info = self.load_ignore_info(os.path.join(base_path, GIT_IGNORE_FILE))
    gitsynchista_ignore_info = self.load_ignore_info(os.path.join(base_path, GITSYNCHISTA_IGNORE_FILE))
    gitsynchista_ignore_info_2 = self.load_ignore_info(os.path.join(base_path, GITSYNCHISTA_IGNORE_FILE_2))
    for f in os.listdir(base_path):
      is_ignored = parent_is_ignored or github_ignore_info.is_ignored(f) or   gitsynchista_ignore_info.is_ignored(f) or gitsynchista_ignore_info_2.is_ignored(f) or global_ignore_info.is_ignored(f) or global_suppress_info.is_ignored(f)
      path = os.path.join(base_path, f)
      attr = os.stat(path)
      isDirectory = os.path.isdir(path)
      if isDirectory:
        if global_suppress_info.is_ignored(f):
          sub_files = None
        else:
          sub_files = self.load_directory(base_path=path, parent_is_ignored=is_ignored)
      else:
        sub_files = None
      
      file = File(name=path.replace(self.root_path, '.', 1), physical_name=path, base_name=f, mtime=attr.st_mtime, sub_files=sub_files, is_ignored=is_ignored)
      files.append(file)
    
    return files
       
  def file_exists(self, path):
    return os.path.exists(path)
    
  def load_ignore_info(self, ignore_file):

    global logger
  
    if self.file_exists(ignore_file):
      ignore_patterns = self.load_into_string(ignore_file)
      logger.info("Loading ignore file '%s'" % ignore_file)    
      return IgnoreInfo(ignore_patterns)
    else:
      return IgnoreInfo('')
   
  def save_from_string(self, path, string):
    with open(path, "wb") as file:
      file.write(string)
  
  def load_into_string(self, path):
    return open(path, "rb").read()
    
  def set_mtime(self, path, mtime):
    os.utime(path, (mtime, mtime))          
    
  def mkdir(self, path):
    os.mkdir(path)
    
  
class WebDavFileAccess(FileAccess):
  
  def __init__(self, webdav_client, root_path=None, conf=None):
    ''' :type conf: sync_config.WebDavConfig
    '''
    super(WebDavFileAccess, self).__init__(root_path)
    self.webdav_client = webdav_client
    self.conf = conf
    
  def file_exists(self, path):
    base_name = os.path.basename(path)
    return False if base_name[0] == '.' else self.webdav_client.exists(path)
    
  def load_directory(self, base_path=None, parent_is_ignored=False):
  
    global logger
    
    if not base_path:
      base_path = self.root_path
    logger.info("Loading WebDav directory '%s'" % base_path)
    files = []
    ignore_info = self.load_ignore_info(os.path.join(base_path, GIT_IGNORE_FILE))
    for f in self.webdav_client.ls(base_path):
      logger.debug("Found remote file '%s'" % f.name)
      if base_path == f.name:
        continue 
      base_name = os.path.basename(f.name)
      is_ignored = parent_is_ignored or ignore_info.is_ignored(base_name) or global_ignore_info.is_ignored(base_name) or global_suppress_info.is_ignored(base_name)
      
      if f.is_dir:
        if global_suppress_info.is_ignored(base_name):
          sub_files = None
        else:
          sub_files = self.load_directory(base_path=f.name, parent_is_ignored=is_ignored)
        mtime = 0
      else:
        sub_files = None
        struct_time = time.strptime(f.mtime, '%a, %d %b %Y %H:%M:%S %Z')
        mtime = time.mktime(struct_time) + self.conf.epoch_delta
      file = File(name=f.name.replace(self.root_path, '.', 1), physical_name=f.name, base_name=base_name, mtime=mtime, sub_files=sub_files, is_ignored=is_ignored)
      files.append(file)
    
    return files
    
  def save_from_string(self, path, string):
    
    global logger
    
    logger.debug("Saving string to WebDav:%s" % path)
    string_file = StringIO.StringIO(string)
    self.webdav_client.upload(string_file, path)
  
  def load_into_string(self, path):
  
    global logger
    
    string_file = StringIO.StringIO()
    self.webdav_client.download(path, string_file)
    logger.debug("Loading 'WebDav:%s' into string" % path)
    return str(string_file.getvalue())

  def set_mtime(self, path, mtime):
    
    global logger
    
    logger.warning("Cannot set mtime for WebDav files")        
    
  def mkdir(self, path):
    self.webdav_client.mkdir(path)
        
def compare_file_sets(file_dict1, file_dict2, change_info):
  for (file_name1, file1) in file_dict1.items():
    if not file1.is_ignored:
      if not file_name1 in file_dict2:
        change_info.new_files.append(file1)
      else:
        file2 = file_dict2[file_name1]
        if (not (file1.is_directory() or file2.is_ignored)) and file1.mtime > file2.mtime:
          change_info.modified_files.append(file1)
  change_info.dest_file_dict = file_dict2

def transfer_modified_files(change_info, source_file_access, dest_file_access):
  
  global logger
  
  for file in change_info.modified_files:
    if not(file.is_directory()):
      dest_file = change_info.dest_file_dict[file.name]
      logger.info("Transferring '%s' to '%s'" % (file.physical_name, dest_file.physical_name))
      dest_file_access.save_from_string(dest_file.physical_name, source_file_access.load_into_string(file.physical_name))
      dest_file_access.set_mtime(dest_file.physical_name, file.mtime)
  
def transfer_new_files(change_info, source_file_access, dest_file_access):
  
  global logger
  
  for file in sorted(change_info.new_files, cmp=compare_files_by_name):
    
    if file.is_ignored:
      continue
        
    dest_physical_name = os.path.normpath(os.path.join(dest_file_access.root_path, file.name))
  
    if file.is_directory():
      logger.info("Creating directory '%s'" % dest_physical_name)
      dest_file_access.mkdir(dest_physical_name)
    else:
      logger.info("Transferring '%s' to '%s'" % (file.physical_name, dest_physical_name))
      dest_file_access.save_from_string(dest_physical_name, source_file_access.load_into_string(file.physical_name))
      dest_file_access.set_mtime(dest_physical_name, file.mtime)

def update_source_timestamps(change_info, source_file_access, dest_file_access):
  
  global logger
  
  updated_dest_files = dest_file_access.load_directory()
  updated_dest_file_dict = make_file_dictionary(updated_dest_files)
  
  all_files = []
  all_files.extend(change_info.modified_files)
  all_files.extend(change_info.new_files)
    
  for file in all_files:
    
    if not file.name in updated_dest_file_dict:
      logger.warning("source file '%s' not found in updated destination file list -> cannot update timestamp" % file.name)
      continue
      
    dest_file = updated_dest_file_dict[file.name]
    if dest_file.mtime > file.mtime:
      logger.info("Updating mtime of '%s' from %s to %s" % (file.name, time.ctime(file.mtime), time.ctime(dest_file.mtime)))
      source_file_access.set_mtime(file.physical_name, dest_file.mtime)
  

class ChangeInfo(object):
  
  def __init__(self):
    
    self.new_files = []
    self.modified_files = []
    self.dest_file_dict = None

class CompareInfo(object):
  
  def __init__(self, local_file_access, remote_file_access):
    
    global logger
    
    self.local_file_access = local_file_access
    self.remote_file_access = remote_file_access
    logger.info("Loading remote directory structure")
    self.remote_files = remote_file_access.load_directory()
    logger.info("Loading local directory structure")
    self.local_files = local_file_access.load_directory()
    self.local_change_info = ChangeInfo()
    self.remote_change_info = ChangeInfo()
    self.compare()

  def compare(self):
  
    self.local_file_dict = make_file_dictionary(self.local_files)
    self.remote_file_dict = make_file_dictionary(self.remote_files)
  
    compare_file_sets(self.local_file_dict, self.remote_file_dict, self.local_change_info)
    compare_file_sets(self.remote_file_dict, self.local_file_dict, self.remote_change_info)

  def transfer_modified_files_to_remote(self):
    transfer_modified_files(self.local_change_info, self.local_file_access, self.remote_file_access)
    
  def transfer_new_files_to_remote(self):
    transfer_new_files(self.local_change_info, self.local_file_access, self.remote_file_access)
    
  def transfer_modified_files_from_remote(self):
    transfer_modified_files(self.remote_change_info, self.remote_file_access, self.local_file_access)
    
  def transfer_new_files_from_remote(self):
    transfer_new_files(self.remote_change_info, self.remote_file_access, self.local_file_access)
    
  def update_local_timestamps(self):
    update_source_timestamps(self.local_change_info, self.local_file_access, self.remote_file_access)

  def get_nr_of_files_to_be_created(self):
    return len(self.local_change_info.new_files) + len(self.remote_change_info.new_files)
    
  def get_nr_of_files_to_be_updated(self):
    return len(self.local_change_info.modified_files) + len(self.remote_change_info.modified_files)

  def is_sync_required(self):
    return (self.get_nr_of_files_to_be_created() + self.get_nr_of_files_to_be_updated()) > 0
      
  def get_sync_summary(self):
    
    if self.is_sync_required():
      
      return "files to be created %d, updates: %d" % (self.get_nr_of_files_to_be_created(), self.get_nr_of_files_to_be_updated()) 
    
    else:
    
      return "all files in sync"
      
  def get_sync_details(self):
    details = "New files and modifications of existing files:"
    label_files_dict = {
      "Local new files": self.local_change_info.new_files,
      "Local modified files": self.local_change_info.modified_files,
      "Remote new files": self.remote_change_info.new_files,
      "Remote modified files": self.remote_change_info.modified_files }
    for label, files in label_files_dict.iteritems():
      if files:
        details += "\n\n{}:\n{}".format(label, "\n".join(
          "    " + file.physical_name for file in files))
    return details
    
def make_file_dictionary(files, file_dict=None):
  
  file_dict = file_dict or {}
  for file in files:
    file_dict[file.name] = file
    if file.sub_files:
      make_file_dictionary(file.sub_files, file_dict)
      
  return file_dict
    

def dump_files(files, indent=0):
  
  global logger

  for f in files:
    logger.debug("%s %s" % (" " * indent, str(f)))
    if f.is_directory():
      dump_files(f.sub_files, indent = indent + 4)

    
class SyncTool(object):
  
  def __init__(self, tool_sync_config):
    
    '''
    :type tool_sync_config: sync_config.SyncConfig
    '''
    self.tool_sync_config = tool_sync_config
    self.compare_info = None
    self.error = None
    self.pyzipista_config_checked = False
    self.pyzipista_config = None
    self.zip_required = True

    if tool_sync_config.repository.working_copy_wakeup:
      self.app_support = working_copy.WorkingCopySupport()
    elif tool_sync_config.repository.auto_open_app:
      self.app_support = url_scheme_support.UrlSchemeSupport(tool_sync_config.repository.auto_open_app)
    else:
      self.app_support = None
    self.check_pyzipista_support()
    
  def get_name(self):
    return self.tool_sync_config.repository.name
    
  def get_webdav_service_name(self):
    return "WebDav Server %s" % self.get_name()
    
    
  def check_open_app(self):
    
    if self.app_support and self.tool_sync_config.repository.auto_open_app:
      self.app_support.open_app()
      
  def check_pyzipista_support(self):
    global logger
    
    if self.pyzipista_config_checked:
      return
      
    self.pyzipista_config_checked = True
    if not pyzipista_support.pyzipista_found():
      logger.info('No pyzipista found')
      return
    
    filename = self.tool_sync_config.repository.local_path
    logger.info('Searching pyzipista config file %s' % filename)
    self.pyzipista_config = pyzipista_support.find_config(filename)
    if self.pyzipista_config:
      logger.info('Found pyzipista config file %s' % filename)
      
  def check_pyzipista(self):
    if not self.pyzipista_config:
      return
      
    self.zip_required = pyzipista_support.load_config_file_and_check_zip_required(self.pyzipista_config)
    
  def execute_pyzipista(self):
    global logger
    
    if not self.pyzipista_config:
      logger.warning("Calling execute pyzipista without available config")
      return
      
    self.zip_required = pyzipista_support.load_config_file_and_zip(self.pyzipista_config)

  def scan(self):    
    global logger
    
    self.error = None
    
    try:
      self.check_open_app()
      self.check_pyzipista()
      
      if self.tool_sync_config.webdav.username:
        username = self.tool_sync_config.webdav.username
        password = self.tool_sync_config.webdav.password
        
        logger.debug('Open WebDAV connection to host %s on port %d for user %s and auth mode %s' % (self.tool_sync_config.webdav.server, self.tool_sync_config.webdav.port, username, self.tool_sync_config.webdav.auth_mode))
        if password == sync_config.PASSWORD_USE_KEY_CHAIN:
          password = util.get_password_from_keychain(self.get_webdav_service_name(), username)

        webdav_client = client.Client(self.tool_sync_config.webdav.server,
                             port=self.tool_sync_config.webdav.port,
                             protocol='http', verify_ssl=False, cert=None, 
                             username=username, password=password,
                             auth_mode=self.tool_sync_config.webdav.auth_mode)
      else:
        logger.debug('Open non-autheticated WebDAV connection to host %s on port %d' % (self.tool_sync_config.webdav.server, self.tool_sync_config.webdav.port))
        webdav_client = client.Client(self.tool_sync_config.webdav.server,
                             port=self.tool_sync_config.webdav.port,
                             protocol='http', verify_ssl=False, cert=None)
                           
      local_file_access = FileAccess(self.tool_sync_config.repository.local_path)
      remote_file_access = WebDavFileAccess(webdav_client, self.tool_sync_config.repository.remote_path, self.tool_sync_config.webdav)      
      self.compare_info = CompareInfo(local_file_access, remote_file_access)
  
      logger.debug("Local files:")
      dump_files(self.compare_info.local_files)
      logger.debug("Remote files:")
      dump_files(self.compare_info.remote_files)
  
      logger.debug("Local new files:")
      for file in self.compare_info.local_change_info.new_files:
        logger.debug("    %s" % str(file))
      logger.debug("Local modified files:")
      for file in self.compare_info.local_change_info.modified_files:
        logger.debug("    %s" % str(file))
      logger.debug("Remote new files:")
      for file in self.compare_info.remote_change_info.new_files:
        logger.debug("    %s" % str(file))
      logger.debug("Remote modified files:")
      for file in self.compare_info.remote_change_info.modified_files:
        logger.debug("    %s" % str(file))

    except Exception as e:
      error_text = str(e)
      logger.error("Error during scan: %s" % error_text)
      self.interpret_error(error_text)
      self.error = error_text

  def auto_scan(self):
    if (self.tool_sync_config.repository.auto_scan and 
        not (self.has_error() or self.is_scanned())):
      self.scan()
      
  def sync(self):
    self.error = None
    
    if not self.compare_info:
      self.scan()
    
    if self.has_error():
      return
    
    try:
      self.check_open_app()
      if self.tool_sync_config.repository.transfer_to_remote:
        self.compare_info.transfer_new_files_to_remote()
        self.compare_info.transfer_modified_files_to_remote()
        self.compare_info.update_local_timestamps()
      
      if self.tool_sync_config.repository.transfer_to_local:
        self.compare_info.transfer_new_files_from_remote()
        self.compare_info.transfer_modified_files_from_remote()
      
      self.compare_info = None
    
    except Exception as e:
      error_text = str(e)
      logger.error("Error during scan: %s" % error_text)
      self.interpret_error(error_text)
      self.error = error_text
    
  def interpret_error(self, error):
      if self.tool_sync_config.webdav.username and '401 Unauthorized' in error:
        self.short_error_text = "Authentication failed"
        logger.info("Authentication error: resetting password in keychain")
        keychain.delete_password(self.get_webdav_service_name(), self.tool_sync_config.webdav.username)
        
      elif 'Connection refused' in error:
        self.short_error_text = "Server unreachable/down"
        
      else:
        self.short_error_text = "Cause unknown"
      
  def is_scanned(self):
    return self.compare_info != None
    
  def working_copy_active(self):
    return self.tool_sync_config.repository.working_copy_wakeup
    
  def is_sync_required(self):
    return self.compare_info.is_sync_required()
    
  def has_error(self):
    return self.error != None
    
  def get_error_text(self):
    return self.error
    
  def get_compare_info(self):
    return self.compare_info
    
  def get_sync_summary(self):
    if self.has_error():
      sync_or_scan = "sync" if self.is_scanned() else "scan"
      return "Error during %s: %s" % (sync_or_scan, self.short_error_text)
      
    else:
      return self.compare_info.get_sync_summary() if self.is_scanned() else "Requires scan"
  
  def get_sync_details(self):
    if self.has_error():
      return self.get_error_text()
      
    else:
      return self.compare_info.get_sync_details()
      
  def open_working_copy_repository(self):
    global logger
    
    if self.working_copy_active():
      self.app_support.open_repository(self.tool_sync_config.repository)
    
    
def find_sync_configs(base_path='..'):
  config_filenames = []
  configs = []
  
  for (dirpath, dirnames, filenames) in os.walk(base_path, topdown=True, onerror=None, followlinks=False):
    for filename in filenames:
      if filename.startswith(GITSYNCHISTA_CONFIG_FILE):
        config_filenames.append( os.path.join(dirpath, filename) )
        
  for filename in config_filenames:
    config_handler = config.ConfigHandler(sync_config.SyncConfig())
    a_sync_config = config_handler.read_config_file(filename)    
    configs.append(a_sync_config)
    
  return configs
  
def test():
  find_sync_configs()
    
if __name__ == '__main__':
  test()