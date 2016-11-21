# coding: utf-8

# https://forum.omz-software.com/topic/3224/tls-ssl-exceptions-from-pythonista-2-1/2

from dropbox import client, session

APP_KEY = 'aaaaaaaaaaaaaaa'
APP_SECRET = 'bbbbbbbbbbbbbbb'
ACCESS_TYPE = 'dropbox'
ACCESS_KEY = 'cccccccccccccccc'
ACCESS_SECRET = 'ddddddddddddddd'

sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
sess.set_token(ACCESS_KEY, ACCESS_SECRET)
client = client.DropboxClient(sess)
folder_metadata = client.metadata('/')
# --------------------
dropbox.dropbox.requests.packages.urllib3.disable_warnings()
# --------------------

