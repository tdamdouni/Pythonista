# coding: utf-8
# This file is part of https://github.com/marcus67/gitsynchista

import webbrowser as wb
import urllib
import time
import keychain
import console

import log
import util
import sync_config
import url_scheme_support

reload(log)
reload(util)
reload(sync_config)
reload(url_scheme_support)

PARAM_IGNORE_WAKEUP = 'IGNORE_WAKEUP'

global logger

logger = log.open_logging(__name__)

class WorkingCopySupport (url_scheme_support.UrlSchemeSupport):
  
  def __init__(self):
    
    super(WorkingCopySupport, self).__init__('working-copy')
    self.key = util.get_password_from_keychain('Working Copy', 'X-URL-Callback')
    
  def wakeup_webdav_server(self):
    
    payload = { 'cmd' : 'start',
                'x-success' : 'pythonista://gitsynchista/gitsynchista?action=run&argv=%s' % PARAM_IGNORE_WAKEUP}
    self._send_to_app(action='webdav', payload=payload, x_callback_enabled=True)
    #time.sleep(1)
    
  def open_repository(self, repository_config):
    
    payload = { 'repo' : repository_config.remote_path[1:]}
    self._send_to_app(action='open', payload=payload)    
    