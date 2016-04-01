# You need the impacket python module (http://corelabs.coresecurity.com)
# Extract the impacket directory to site-packages (https://pypi.python.org/packages/source/i/impacket/)
# and you also need a copy of ntpath.py in your site-package directory

import ui, os, shutil
import sys
import string
import time
from impacket import smb, version, smb3, nt_errors
from impacket.dcerpc.v5 import samr, transport, srvs
from impacket.dcerpc.v5.dtypes import NULL
from impacket.smbconnection import *
import time

class SMBclient(object):

  def __init__(self):
    self.fileName = ''
    self.localFile = ''
    self.remoteFile = ''
    self.smb = None
    self.pwd = ''
    self.share = None
    self.loggedIn = False
    self.password = None
    self.username = None
    self.host = None 
    self.root = os.path.expanduser('~')
    self.path = os.getcwd()
    self.view = ui.load_view('PhoneSMB')
    self.subview = self.view['scrollview1'].subviews
    for i in range(0, len(self.subview)):
      #print self.subview[i].name
      if self.subview[i].name == 'bt_connect':
        self.sv_bt_connect = self.subview[i]
      elif self.subview[i].name == 'bt_transfer':
        self.sv_bt_transfer = self.subview[i]
      elif self.subview[i].name == 'bt_delete':
        self.sv_bt_delete = self.subview[i]
      elif self.subview[i].name == 'bt_mkdir':
        self.sv_bt_mkdir = self.subview[i]
      elif self.subview[i].name == 'bt_rmdir':
        self.sv_bt_rmdir = self.subview[i]
      elif self.subview[i].name == 'bt_rename':
        self.sv_bt_rename = self.subview[i]
      elif self.subview[i].name == 'bt_connect':
        self.sv_bt_connect = self.subview[i]
      elif self.subview[i].name == 'tv_info':
        self.sv_tv_info = self.subview[i]
      elif self.subview[i].name == 'tv_local':
        self.sv_tv_local = self.subview[i]
      elif self.subview[i].name == 'tv_remote':
        self.sv_tv_remote = self.subview[i]
      elif self.subview[i].name == 'lb_local':
        self.sv_lb_local = self.subview[i]
      elif self.subview[i].name == 'lb_remote':
        self.sv_lb_remote = self.subview[i]
    self.side = 'local'
    self.sv_tv_local.border_color = '#ff0000'
    self.sv_bt_connect.action = self.bt_connect
    self.sv_bt_transfer.action = self.bt_transfer
    self.sv_bt_delete.action = self.bt_delete
    self.sv_bt_mkdir.action = self.bt_mkdir
    self.sv_bt_rmdir.action = self.bt_rmdir
    self.sv_bt_rename.action = self.bt_rename
    self.root_len = len(self.root)
    path = self.path[self.root_len:]
    pos = path.rfind('/')   #+ 1
    self.sv_lb_local.text = path[pos:]
    all = self.get_dir()
    self.lst_local = ui.ListDataSource(all)
    self.sv_tv_local.data_source = self.lst_local
    self.sv_tv_local.delegate = self.lst_local
    self.sv_tv_local.editing = False
    self.lst_local.font = ('Courier',14)
    self.lst_local.action = self.table_local_tapped
    self.lst_local.delete_enabled = False 
    self.lst_remote = ui.ListDataSource([''])
    self.sv_tv_remote.data_source = self.lst_remote
    self.sv_tv_remote.delegate = self.lst_remote
    self.sv_tv_remote.editing = False
    self.lst_remote.font = ('Courier',14)
    self.lst_remote.action = self.table_remote_tapped
    self.lst_remote.delete_enabled = False 
    self.view.present('fullscreen')

  def is_root(self, path):
    if len(path) == 1:
      if path == '/' or path == '\\':
        return True
    return False

  def open_popover_view(self, view_name, view_title):
    self.view_po = ui.load_view(view_name)
    self.view_po.name = view_title
    #self.view_po.present('popover',popover_location=(self.view.width/2,self.view.height/2))
    self.view.hidden = True
    self.view_po.present('fullscreen')
    self.view_po['bt_cancel'].action = self.bt_cancel
    #self.view_po.width = 320
    #self.view_po.height = 504
  
  ### Rename ###
  def bt_rename(self, sender):
    if self.side == 'local':
      self.open_popover_view('popover', 'Rename local file?')
      pos = self.localFile.rfind('/')
      self.fileName = self.localFile[pos+1:]
      self.view_po['lb_old_name'].text = self.fileName
      self.view_po['tf_new_name'].text = self.fileName
      self.view_po['bt_okay'].action = self.bt_local_rename_okay
    if self.loggedIn and self.side == 'remote':
      self.open_popover_view('popover', 'Rename remote file?')
      pos = self.remoteFile.rfind('\\')
      self.fileName = self.remoteFile[pos+1:]
      self.view_po['lb_old_name'].text = self.fileName
      self.view_po['tf_new_name'].text = self.fileName
      self.view_po['bt_okay'].action = self.bt_remote_rename_okay

  def bt_local_rename_okay(self, sender):
    #print self.fileName
    #print self.view_po['tf_new_name'].text
    os.rename(self.path + '/' + self.fileName, self.path + '/' + self.view_po['tf_new_name'].text)
    self.view_po.close()
    self.view.hidden = False
    all = self.get_dir()
    self.refresh_table(self.sv_tv_local,self.lst_local,all)

  def bt_remote_rename_okay(self, sender):
    self.smb.rename(self.share, self.remoteFile, self.pwd + '\\' + self.view_po['tf_new_name'].text)
    self.view_po.close()
    self.view.hidden = False
    all = self.get_remote_dir()
    self.refresh_table(self.sv_tv_remote,self.lst_remote,all)

  def bt_cancel(self, sender):
    self.view_po.close()
    self.view.hidden = False

  ### Delete ###
  def bt_delete(self, sender):
    if self.side == 'local':
      self.open_popover_view('select', 'Delete local file(s)?')
      if len(self.localFile) > 0:
        pos = self.localFile.rfind('/')
        self.fileName = self.localFile[pos+1:]
      else:
        self.fileName = self.path[self.root_len:]
        self.view_po['sc_range'].selected_index = 2
      self.view_po['tf_name'].text = self.fileName
      self.view_po['tf_name'].enabled = False
      self.view_po['bt_okay'].action = self.bt_select_okay_local_delete
    if self.loggedIn and self.side == 'remote':
      self.open_popover_view('select', 'Delete remote file(s)?')
      if len(self.remoteFile) > 0:
        pos = self.remoteFile.rfind('\\')
        self.fileName = self.remoteFile[pos+1:]
      else:
        self.fileName = self.pwd
        self.view_po['sc_range'].selected_index = 2
      self.view_po['tf_name'].text = self.fileName
      self.view_po['tf_name'].enabled = False
      self.view_po['bt_okay'].action = self.bt_select_okay_remote_delete

  def bt_select_okay_local_delete(self, sender):
    rang = self.view_po['sc_range'].selected_index
    if rang == 0: # selected file
      files = self.get_files()
    elif rang == 1: # all files
      files = self.get_files(filter='*.*')
    elif rang == 2: # filter
      files = self.get_files(filter=self.view_po['tf_filter'].text)
    if len(files) > 0:  
      for file in files:
        try:
          os.remove(self.path + '/' + file)
          self.localFile = ''
        except Exception, e:
          self.tv_info.text += '\n' + str(e)
      all = self.get_dir()
      self.refresh_table(self.sv_tv_local,self.lst_local,all)
    self.view_po.close()
    self.view.hidden = False
      
  def bt_select_okay_remote_delete(self, sender):
    rang = self.view_po['sc_range'].selected_index
    if rang == 0: # selected file
      files = self.get_files(local=False)
    elif rang == 1: # all files
      files = self.get_files(filter='*.*', local=False)
    elif rang == 2: # filter
      files = self.get_files(filter=self.view_po['tf_filter'].text, local=False)
    if len(files) > 0:  
      for file in files:
        try:
          self.smb.deleteFile(self.share, self.pwd + '\\' + file)
          self.remoteFile = ''
        except Exception, e:
          self.sv_tv_info.text += '\n' + str(e)
      all = self.get_remote_dir()
      self.refresh_table(self.sv_tv_remote,self.lst_remote,all)
    self.view_po.close()
    self.view.hidden = False

  def get_files(self, filter=None, local=True):
    files = []
    if filter == None:
      if local and self.localFile != '' or not local and self.remoteFile != '':
        files = [self.view_po['tf_name'].text]
      else:
        self.sv_tv_info.text += "\nNo file selected to delete."
    else:
      #check filter
      if filter[0] != '*' and filter[1] != '.':
        self.sv_tv_info.text += "\nFilter not valid! It has to start with *."
        return files
      if not local:
        entries = self.smb.listPath(self.share, self.pwd + '\\' + filter)
        filter = filter[1:]
        for e in entries:
          if e.is_directory() == 0:
            entry = str(e.get_longname())
            if filter == '.*': # all files
              files.append(entry)
            else: # filtered files
              filter_len = len(filter)
              entry_len = len(entry)
              if entry.find(filter) == entry_len-filter_len:
                files.append(entry)
      else:
        filter = filter[1:]
        for entry in sorted(os.listdir(self.path)):
          if os.path.isfile(self.path + '/' + entry):
            if filter == '.*': # all files
              files.append(entry)
            else: # filtered files
              filter_len = len(filter)
              entry_len = len(entry)
              if entry.find(filter) == entry_len-filter_len:
                files.append(entry)
    return files

  ### MkDir ###
  def bt_mkdir(self, sender):
    if self.side == 'local':
      self.open_popover_view('popover', 'Make local directory?')
      self.view_po['lb_old_name'].text = self.path[self.root_len:] + '/'
      self.view_po['lb_on'].text = 'Path:'
      self.view_po['lb_nn'].text = 'New Dir:'
      self.view_po['bt_okay'].action = self.bt_local_mkdir_okay
    if self.loggedIn and self.side == 'remote':
      self.open_popover_view('popover', 'Make remote directory?')
      if self.is_root(self.pwd):
        self.view_po['lb_old_name'].text = self.pwd
      else:
        self.view_po['lb_old_name'].text = self.pwd + '\\'
      self.view_po['lb_on'].text = 'Path:'
      self.view_po['lb_nn'].text = 'New Dir:'
      self.view_po['bt_okay'].action = self.bt_remote_mkdir_okay

  def bt_local_mkdir_okay(self, sender):
    directory = self.view_po['tf_new_name'].text
    os.mkdir(self.path + '/' + directory)
    self.view_po.close()
    self.view.hidden = False
    all = self.get_dir()
    self.refresh_table(self.sv_tv_local,self.lst_local,all)

  def bt_remote_mkdir_okay(self, sender):
    directory = self.view_po['tf_new_name'].text
    if self.is_root(self.pwd):
      self.smb.createDirectory(self.share,self.pwd + directory)
    else:
      self.smb.createDirectory(self.share,self.pwd + '\\' + directory)
    self.view_po.close()
    self.view.hidden = False
    all = self.get_remote_dir()
    self.refresh_table(self.sv_tv_remote,self.lst_remote,all)

  ### RmDir ###
  def bt_rmdir(self, sender):
    if self.side == 'local':
      self.open_popover_view('popover', 'Remove local directory?')
      self.view_po['lb_old_name'].text = self.path[self.root_len:] + '/'
      self.view_po['lb_on'].text = 'Path:'
      self.view_po['lb_nn'].text = 'Remove Dir:'
      self.view_po['bt_okay'].action = self.bt_local_rmdir_okay
    if self.loggedIn and self.side == 'remote':
      self.open_popover_view('popover', 'Remove remote directory?')
      if self.is_root(self.pwd):
        self.view_po['lb_old_name'].text = self.pwd
      else:
        self.view_po['lb_old_name'].text = self.pwd + '\\'
      self.view_po['lb_on'].text = 'Path:'
      self.view_po['lb_nn'].text = 'Remove Dir:'
      self.view_po['bt_okay'].action = self.bt_remote_rmdir_okay

  def bt_local_rmdir_okay(self, sender):
    shutil.rmtree(self.path)
    pos = self.path.rfind('/')
    dir = self.path[:pos]
    self.path = dir
    path = self.path[self.root_len:]
    pos = path.rfind('/')   #+ 1
    self.sv_lb_local.text = path[pos:]
    all = self.get_dir()
    self.refresh_table(self.sv_tv_local,self.lst_local,all)
    self.view_po.close()
    self.view.hidden = False

  def bt_remote_rmdir_okay(self, sender):
    directory = self.view_po['tf_new_name'].text
    if self.is_root(self.pwd) and directory == '':
      self.sv_tv_info.text += "\nSorry, root directory is not removable."
    else:
      try:
        self.smb.deleteDirectory(self.share,self.pwd + '\\' + directory)
        pos = self.pwd.rfind('\\')
        self.pwd = self.pwd[:pos]
        pos = self.pwd.rfind('\\')
        self.sv_lb_remote.text = self.pwd[pos:]
      except Exception, e:
        self.sv_tv_info.text += '\n' + str(e)
    self.view_po.close()
    self.view.hidden = False
    all = self.get_remote_dir()
    self.refresh_table(self.sv_tv_remote,self.lst_remote,all)

  ### Connect ###
  def bt_connect(self, sender):
    self.open_popover_view('connect', 'Connect')
    self.view_po['bt_connect'].action = self.bt_connect_okay
    if self.loggedIn:
      self.view_po['bt_connect'].title = 'Disconnect'
    
  def bt_connect_okay(self, sender):
    hostshare = self.view_po['tf_host'].text
    if hostshare.find('/') > 0:
      self.host, self.share = hostshare.split('/')
    self.username = self.view_po['tf_user'].text
    self.password = self.view_po['tf_password'].text
    
    if self.loggedIn is False:
      try:
        self.smb = SMBConnection('*SMBSERVER', self.host, sess_port=139)
        dialect = self.smb.getDialect()
        if dialect == SMB_DIALECT:
          self.sv_tv_info.text = "SMBv1 dialect used"
        elif dialect == SMB2_DIALECT_002:
          self.sv_tv_info.text = "SMBv2.0 dialect used"
        elif dialect == SMB2_DIALECT_21:
          self.sv_tv_info.text = "SMBv2.1 dialect used"
        else:
          self.sv_tv_info.text = "SMBv3.0 dialect used"
        if self.smb is None:
          self.sv_tv_info.text = "No connection open"
          return
        self.smb.login(self.username, self.password, domain='')
        if self.smb.isGuestSession() > 0:
          self.sv_tv_info.text += "\nGUEST Session Granted"
        else:
          self.sv_tv_info.text += "\nUSER Session Granted"
        self.loggedIn = True
        self.smb.connectTree(self.share)
        self.pwd = '\\'
        all = self.get_remote_dir()
        self.refresh_table(self.sv_tv_remote,self.lst_remote,all)
        self.sv_lb_remote.text = self.pwd
        self.view_po.close()
        self.view.hidden = False
      except Exception, e:
        self.sv_tv_info.text += '\n' + str(e)
        self.loggedIn = False 
        self.view_po.close()
        self.view.hidden = False
    else:
      if self.smb is not None:
        del(self.smb);
      self.share = None
      self.pwd = ''
      self.loggedIn = False
      self.password = None
      self.username = None
      sender.title = 'Connect'
      self.sv_tv_info.text += "\nConnection closed"
      self.view_po.close()
      self.sv_tv_remote.data_source = []
      self.side = 'local'
      self.sv_tv_local.border_color = '#ff0000'
      self.sv_tv_remote.border_color = '#0000ff'
      self.sv_lb_remote.text = 'Remote'
      self.view.hidden = False

  ### Transfer ###
  def bt_transfer(self, sender):
    if self.loggedIn:
      if self.side == 'remote':
        self.open_popover_view('select', 'Download remote file(s)?')
        pos = self.remoteFile.rfind('\\')
        fileName = self.remoteFile[pos+1:]
        self.view_po['tf_name'].text = fileName
        self.view_po['tf_name'].enabled = False
        self.view_po['bt_okay'].action = self.bt_select_okay_get
      else:
        self.open_popover_view('select', 'Upload local file(s)?')
        if len(self.localFile) > 0:
          pos = self.localFile.rfind('/')
          self.fileName = self.localFile[pos+1:]
        else:
          self.fileName = self.path[self.root_len:]
          self.view_po['sc_range'].selected_index = 1
        self.view_po['tf_name'].text = self.fileName
        self.view_po['tf_name'].enabled = False
        self.view_po['bt_okay'].action = self.bt_select_okay_put

  def bt_select_okay_get(self, sender):
    rang = self.view_po['sc_range'].selected_index
    if rang == 0: # selected file
      files = self.get_files(local=False)
    elif rang == 1: # all files
      files = self.get_files(filter='*.*', local=False)
    elif rang == 2: # filter
      files = self.get_files(filter=self.view_po['tf_filter'].text, local=False)
    if len(files) > 0:  
      for file in files:
        fh = open(self.path + '/' + file,'wb')
        try:
          self.smb.getFile(self.share, self.pwd + '\\' + file, fh.write)
        except:
          fh.close()
          os.remove(self.path + '/' + file)
        fh.close()
      all = self.get_dir()
      self.refresh_table(self.sv_tv_local,self.lst_local,all)
    self.view_po.close()
    self.view.hidden = False
    
  def bt_select_okay_put(self, sender):
    rang = self.view_po['sc_range'].selected_index
    if rang == 0: # selected file
      files = self.get_files()
    elif rang == 1: # all files
      files = self.get_files(filter='*.*')
    elif rang == 2: # filter
      files = self.get_files(filter=self.view_po['tf_filter'].text)
    if len(files) > 0:  
      for file in files:
        fh = open(self.path + '/' + file, 'rb')
        if self.is_root(self.pwd):
          self.smb.putFile(self.share, self.pwd + file, fh.read)
        else:
          self.smb.putFile(self.share, self.pwd + '\\' + file, fh.read)
        fh.close()
      all = self.get_remote_dir()
      self.refresh_table(self.sv_tv_remote,self.lst_remote,all)
    self.view_po.close()
    self.view.hidden = False

  ### TableViews ###
  def table_local_tapped(self, sender):
    self.side = 'local'
    self.sv_tv_local.border_color = '#ff0000'
    self.sv_tv_remote.border_color = '#0000ff'
    rowtext = sender.items[sender.selected_row]
    filename_tapped = rowtext
    if rowtext[0] == '/':
      if filename_tapped == '/..':
        pos = self.path.rfind('/')
        self.path = self.path[:pos]
      else:
        self.path = self.path + filename_tapped
      self.localFile = ''
      all = self.get_dir()
      root_len = len(self.root)
      #self.sv_lb_local.text = self.path[root_len:]
      path = self.path[root_len:]
      pos = path.rfind('/')  #+1
      self.sv_lb_local.text = path[pos:]      
      self.refresh_table(self.sv_tv_local,self.lst_local,all)
    else:
      self.localFile = self.path + '/' + filename_tapped

  def table_remote_tapped(self, sender):
    if self.loggedIn:
      self.side = 'remote'
      self.sv_tv_remote.border_color = '#ff0000'
      self.sv_tv_local.border_color = '#0000ff'
      rowtext = sender.items[sender.selected_row]
      filename_tapped = rowtext
      if rowtext[0] == '\\': #directory
        if filename_tapped == '\\..': # up
          pos = self.pwd.rfind('\\')
          self.pwd = self.pwd[:pos]
          if self.pwd == '':
            self.pwd = '\\'
        else:
          if self.is_root(self.pwd):
            self.pwd = filename_tapped
          else:
            self.pwd += filename_tapped
        self.remoteFile = ''
        all = self.get_remote_dir()
        self.refresh_table(self.sv_tv_remote,self.lst_remote,all)
        pos = self.pwd.rfind('\\')
        self.sv_lb_remote.text = self.pwd[pos:]
      else: # file
        self.remoteFile = self.pwd + '\\' + filename_tapped

  def refresh_table(self, table, lst, data):
    lst = ui.ListDataSource(data)
    table.data_source = lst
    table.delegate = lst
    table.editing = False
    lst.font = ('Courier',14)
    if table.name == 'tv_local':
      lst.action = self.table_local_tapped
    else:
      lst.action = self.table_remote_tapped
    lst.delete_enabled = False 
    table.reload_data()
    return

  def get_dir(self):
    dirs  = [] if self.path == self.root else ['..']
    files = []
    for entry in sorted(os.listdir(self.path)):
      if os.path.isdir(self.path + '/' + entry):
        dirs.append(entry)
      else:
        files.append(entry)
    all = ['/' + dir for dir in dirs]
    for file in files:
      full_pathname = self.path + '/' + file
      all.append('{}'.format(file))
    return all

  def get_remote_dir(self):
    if self.loggedIn:
      remoteDir  = [] if self.pwd == '\\' else ['\\..']
      files = []
      entries = self.smb.listPath(self.share, self.pwd + '\\*')
      for e in entries:
        if e.is_directory() > 0:
          if str(e.get_longname()) != '.' and str(e.get_longname()) != '..':
            remoteDir.append('\\' + str(e.get_longname()))
        else:
          files.append(str(e.get_longname()))
      all = sorted(remoteDir)
      for file in sorted(files):
        all.append('{}'.format(file))
      return all
    else:
      self.pwd = ''
      return []
    
    #e.get_filesize()
    #time.ctime(float(e.get_mtime_epoch()))

SMBclient()
