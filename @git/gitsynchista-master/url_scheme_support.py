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

reload(log)
reload(util)
reload(sync_config)

PARAM_IGNORE_WAKEUP = 'IGNORE_WAKEUP'

global logger

logger = log.open_logging(__name__)

class UrlSchemeSupport (object):
  
  def __init__(self, app_name):
    
    self.app_name = app_name
    self.key = None
      
  def _send_to_app(self, action='', payload={}, x_callback_enabled=False):
    
    # see https://github.com/ahenry91/wc_sync
    
    global logger
    
    if not self.app_name:
      logger.warning("Trying to use url scheme without app name. Ignoring request.")
      return
      
    logger.debug("_send_to_app: action=%s, x_callback_enabled=%s, playload=%s" % (action, str(x_callback_enabled), str(payload)))
      
    x_callback = 'x-callback-url/' if x_callback_enabled else ''
    if self.key:
      payload['key'] = self.key
    if len(payload) > 0:
      payload_string = '/?' + urllib.urlencode(payload).replace('+', '%20')
    else:
      payload_string = ''
    fmt = '{app_name}://{x_callback}{action}{payload}'
    url = fmt.format(app_name=self.app_name, x_callback=x_callback, action=action, payload=payload_string)
    
    logger.debug("Opening url '%s'" % url)
    
    wb.open(url)  
    
  def open_app(self):
    
    self._send_to_app()
    time.sleep(2)
    
  def wakeup_webdav_server(self):
    
    pass
    
  def open_repository(self, repository_config=None):
    
    pass
    
    