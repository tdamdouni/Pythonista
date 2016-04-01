# coding: utf-8

# https://gist.github.com/woolsweater/9f19bd28d944d1120353

# Overwrite directory in Pythonista with Working Copy repo of the same name
import os
import sys
import urllib
from base64 import b64decode
from zipfile import ZipFile
from cStringIO import StringIO
from uuid import uuid4 as uuid

import editor
import console
import keychain
import webbrowser

# Set to true and run script to force entry of a new URL key
RENEW_WC_CALLBACK_KEY = False

def path_after_docs_dir(pth):
    return pth.split("Documents/", 1)[-1]
    
def last_dir_in_path(pth):
    return os.path.basename(os.path.normpath(os.path.dirname(pth)))
    
def WC_callback_key(overwrite_key=False):
    service = "Working Copy"
    # UUID appended to avoid collision with another script
    # (generated on original dev machine)
    account = "x_callback_url_6653ee08-4c43-4453-a400-c5de315b0725"
    key = keychain.get_password(service, account)
    if overwrite_key or not key:
        key = console.input_alert("Enter Working Copy URL key:")
        keychain.set_password(service, account, key)
    return key

# Arriving here as callback
if len(sys.argv) > 1:
    action = sys.argv[1]
    # Success
    if action == "unpack":
        dest_dir = sys.argv[2]
        data = sys.argv[3]
        # Receive zipped repo, unpack
        archive = ZipFile(StringIO(b64decode(data)))
        # Overwrite directory (asking?)
        archive.extractall(dest_dir)
        # Refresh editor after unpacking 
        editor.reload_files()
        editor.open_file(editor.get_path())
# Run as action
else:
    # Get path to directory of script from which action was run; this will be 
    # the install directory, passed to the script when it's called back
    dest_dir = os.path.dirname(editor.get_path())
    # The name of the repo in WC is assumed to be the same as the closest 
    # enclosing directory from the activating script
    repo_name = os.path.basename(dest_dir)
    # Path of this retrieval script starting from Pythonista's Documents
    # directory, for the pythonista://<script-name> URL
    self_pth = path_after_docs_dir(__file__)
    
    success_action = "pythonista://{}?action=run&argv=unpack&argv={}&argv="
    success_action = success_action.format(self_pth, dest_dir)
    command = "zip"
    URL_key = WC_callback_key(RENEW_WC_CALLBACK_KEY)
    url_args = urllib.urlencode({ "x-success" : success_action,
                                  "key" : URL_key,
                                  "repo" : repo_name})
    x_callback_url = "working-copy://x-callback-url/{command}/?{url_args}"
    x_callback_url = x_callback_url.format(command=command, url_args=url_args)
    webbrowser.open(x_callback_url)  