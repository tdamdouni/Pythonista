# YOU NEED TO INSERT YOUR APP KEY AND SECRET BELOW!
# Go to dropbox.com/developers/apps to create an app.
import keychain

# Put your settings below if you don't have a login script.
app_key = keychain.get_password('dropbox', 'app_key')
app_secret = keychain.get_password('dropbox', 'app_secret')

# access_type can be 'app_folder' or 'dropbox', depending on
# how you registered your app.
access_type = 'app_folder'

import webbrowser
from dropbox import client, rest, session
import keychain
import pickle
import console

def get_request_token():
	console.clear()
	print 'Getting request token...'	
	sess = session.DropboxSession(app_key, app_secret, access_type)
	request_token = sess.obtain_request_token()
	url = sess.build_authorize_url(request_token)
	console.clear()
	webbrowser.open(url, modal=True)
	return request_token

def get_access_token():
	token_str = keychain.get_password('dropbox', app_key)
	if token_str:
		key, secret = pickle.loads(token_str)
		return session.OAuthToken(key, secret)
	request_token = get_request_token()
	sess = session.DropboxSession(app_key, app_secret, access_type)
	access_token = sess.obtain_access_token(request_token)
	token_str = pickle.dumps((access_token.key, access_token.secret))
	keychain.set_password('dropbox', app_key, token_str)
	return access_token

def get_client():
	access_token = get_access_token()
	sess = session.DropboxSession(app_key, app_secret, access_type)
	sess.set_token(access_token.key, access_token.secret)
	dropbox_client = client.DropboxClient(sess)
	return dropbox_client

def main():
	# Demo if started run as a script...
	# Just print the account info to verify that the authentication worked:
	print 'Getting account info...'
	dropbox_client = get_client()
	account_info = dropbox_client.account_info()
	print 'linked account:', account_info

if __name__ == '__main__':
    main()
