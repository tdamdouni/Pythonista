import sys
import client
import os
import time
import datetime
import logging
import re
import tempfile
import StringIO

import config
import sync_config

reload(client)
reload(logging)
reload(config)
reload(sync_config)

GIT_IGNORE_FILE = '.gitignore'
GITSYNCHISTA_IGNORE_FILE = 'gitsynchista_ignore'
GITSYNCHISTA_CONFIG_FILE = 'gitsynchista_config'

ADDITIONAL_IGNORE_PATTERNS = '|\..*'

global logger

logger = logging.getLogger('gitsynchista')  
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

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
    return "log=%s phys=%s dir=%s ign=%s %s" % (self.name, self.physical_name, self.is_directory(), self.is_ignored, time.ctime(self.mtime))
    
def compare_files_by_name(file1, file2):
  return cmp(file1.name, file2.name)
  
class IgnoreInfo(object):
  
  def __init__(self, file_string):
    
    global logger
    
    pattern_string = ('^' + file_string.replace('.','\.').replace('*', '.*').replace('\n','$|^') + '$').replace('|^$', '') + ADDITIONAL_IGNORE_PATTERNS
    logger.info("Created IgnoreInfo with pattern regex '%s'" % pattern_string)
    self.regex = re.compile(pattern_string)        
    
  def is_ignored(self, name):
    
    return self.regex.match(name) != None
    
class FileAccess(object):
  
  def __init__(self, root_path):
    
    self.root_path = root_path
  
  def load_directory(self, base_path=None, parent_is_ignored=False):
    
    if not base_path:
      base_path = self.root_path
    logger.info("Loading file directory '%s'" % base_path)
    files = []
    github_ignore_info = self.load_ignore_info(os.path.join(base_path, GIT_IGNORE_FILE))
    gitsynchista_ignore_info = self.load_ignore_info(os.path.join(base_path, GITSYNCHISTA_IGNORE_FILE))
    for f in os.listdir(base_path):
      is_ignored = parent_is_ignored or (github_ignore_info != None and github_ignore_info.is_ignored(f)) or (gitsynchista_ignore_info != None and gitsynchista_ignore_info.is_ignored(f))
      path = os.path.join(base_path, f)
      attr = os.stat(path)
      isDirectory = os.path.isdir(path)
      if isDirectory:
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
      return None
   
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
  
  def __init__(self, webdav_client, root_path=None):
    
    super(WebDavFileAccess, self).__init__(root_path)
    self.webdav_client = webdav_client
    
  def file_exists(self, path):
    base_name = os.path.basename(path)
    if base_name[0] == '.':
      return False
    else:
      return self.webdav_client.exists(path)
    
  def load_directory(self, base_path=None, parent_is_ignored=False):
  
    global logger
    
    if not base_path:
      base_path = self.root_path
    logger.info("Loading WebDav directory '%s'" % base_path)
    files = []
    ignore_info = self.load_ignore_info(os.path.join(base_path, GIT_IGNORE_FILE))
    for f in self.webdav_client.ls(base_path):
      if base_path == f.name:
        continue 
      base_name = os.path.basename(f.name)
      is_ignored = parent_is_ignored or (ignore_info != None and ignore_info.is_ignored(base_name))
      #print f.name
      if f.mtime == '':
        sub_files = self.load_directory(base_path=f.name, parent_is_ignored=is_ignored)
        mtime = 0
      else:
        sub_files = None
        struct_time = time.strptime(f.mtime, '%a, %d %b %Y %H:%M:%S %Z')
        mtime = time.mktime(struct_time) + 3600
      file = File(name=f.name.replace(self.root_path, '.', 1), physical_name=f.name, base_name=base_name, mtime=mtime, sub_files=sub_files, is_ignored=is_ignored)
      files.append(file)
    
    return files
    
  def save_from_string(self, path, string):
    
    global logger
    
    logger.info("Saving string to WebDav:%s" % path)
    string_file = StringIO.StringIO(string)
    self.webdav_client.upload(string_file, path)
  
  def load_into_string(self, path):
  
    global logger
    
    string_file = StringIO.StringIO()
    self.webdav_client.download(path, string_file)
    logger.info("Loading 'WebDav:%s' into string" % path)
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
      #logger.warning("Creation of directories not supported yet: create '%s' manually" % file.name)
      #continue
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
      logger.warning("source file '%s' not found in upated destination file list -> cannot update timestamp" % file.name)
      continue
      
    dest_file = updated_dest_file_dict[file.name]
    if dest_file.mtime > file.mtime:
      logger.info("updating mtime of '%s' from %s to %s" % (file.name, time.ctime(file.mtime), time.ctime(dest_file.mtime)))
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

    
    
def make_file_dictionary(files, file_dict=None):
  
  if not file_dict:
    file_dict = {}
  for file in files:
    file_dict[file.name] = file
    if file.sub_files:
      make_file_dictionary(file.sub_files, file_dict)
      
  return file_dict
    

def dump_files(files, indent=0):
  
  global logger

  for f in files:
    logger.info("%s %s" % (" " * indent, str(f)))
    if f.is_directory():
      dump_files(f.sub_files, indent = indent + 4)

    
class SyncTool(object):
  
  def __init__(self, tool_sync_config):
    
    self.tool_sync_config = tool_sync_config
    self.compare_info = None
    
  def scan(self):
    
    global logger

    webdav_client = client.Client(self.tool_sync_config.webdav.server, port=self.tool_sync_config.webdav.port,
                   protocol='http', verify_ssl=False, cert=None, username=self.tool_sync_config.webdav.username, password=self.tool_sync_config.webdav.password)
    local_file_access = FileAccess(self.tool_sync_config.repository.local_path)
    remote_file_access = WebDavFileAccess(webdav_client, self.tool_sync_config.repository.remote_path)    
  
    self.compare_info = CompareInfo(local_file_access, remote_file_access)
  
    logger.info("Local files:")
    dump_files(self.compare_info.local_files)
    logger.info("Remote files:")
    dump_files(self.compare_info.remote_files)
  
    logger.info("Local new files:")
    for file in self.compare_info.local_change_info.new_files:
      logger.info("    %s" % str(file))
    logger.info("Local modified files:")
    for file in self.compare_info.local_change_info.modified_files:
      logger.info("    %s" % str(file))
    logger.info("Remote new files:")
    for file in self.compare_info.remote_change_info.new_files:
      logger.info("    %s" % str(file))
    logger.info("Remote modified files:")
    for file in self.compare_info.remote_change_info.modified_files:
      logger.info("    %s" % str(file))


  def sync(self):
    
    if self.compare_info == None:
      self.scan()
      
    if self.tool_sync_config.repository.transfer_to_remote:
      self.compare_info.transfer_new_files_to_remote()
      self.compare_info.transfer_modified_files_to_remote()
      self.compare_info.update_local_timestamps()
      
    if self.tool_sync_config.repository.transfer_to_local:
      self.compare_info.transfer_new_files_from_remote()
      self.compare_info.transfer_modified_files_from_remote()
  

def find_sync_configs(base_path='..'):
  
  config_filenames = []
  configs = []
  
  for (dirpath, dirnames, filenames) in os.walk(base_path, topdown=True, onerror=None, followlinks=False):
    
    for filename in filenames:
      
      if filename == GITSYNCHISTA_CONFIG_FILE:
        config_filenames.append( os.path.join(dirpath, filename) )
        
  for filename in config_filenames:
    config_handler = config.ConfigHandler(sync_config.SyncConfig())
    a_sync_config = config_handler.read_config_file(filename)    
    configs.append(a_sync_config)
    
  return configs
  
  
def load_config_file_and_sync(config_filename):
  
  global logger
  
  config_handler = config.ConfigHandler(sync_config.SyncConfig())
  tool_sync_config = config_handler.read_config_file(config_filename)
  
  sync_tool = SyncTool(tool_sync_config)
  
  try:
    
    sync_tool.scan()
    
  except Exception as e:
    
    logger.error("Exception %s during scan" % str(e))
    return
  
  try:
    
    sync_tool.sync()
    
  except Exception as e:
    
    logger.error("Exception %s during sync" % str(e))
  

def start_gui():
  
  global logger
  
  sync_tools = []
  logger.info("Starting GUI...")
  configs = find_sync_configs()
  for config in configs:
    
    logger.info("Found configuration '%s'..." % config.repository.name)
    
    try:
      
      sync_tool = SyncTool(config)
      sync_tool.scan()
      sync_tools.append(sync_tool)
      
    except Exception as e:
      
      logger.info("Error '%s' while processing configuration '%s'" % ( str(e), config.repository.name) )
    
      
  
def main():
  
  if len(sys.argv) == 2:  
    load_config_file_and_sync(sys.argv[1])
  else:
    start_gui()
  
if __name__ == '__main__':
  main()
  
