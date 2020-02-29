from __future__ import print_function
# https://forum.omz-software.com/topic/3214/dropbox-module-and-access-token/3

from dropbox import client, rest, session
APP_KEY = 'my_key_is_here'
APP_SECRET = 'my_secret_is_here'
ACCESS_TYPE = 'dropbox'
sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
request_token = sess.obtain_request_token()
url = sess.build_authorize_url(request_token)
# Make the user sign in and authorize this token
print("url:", url)
print("Please visit this website and press the 'Allow' button, then hit 'Enter' here.")
raw_input()
# This will fail if the user didn't visit the above URL and hit 'Allow'
access_token = sess.obtain_access_token(request_token)
client = client.DropboxClient(sess)
print("linked account:", client.account_info())

# --------------------
