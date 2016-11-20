# https://gist.github.com/KainokiKaede/f2f4dbf2bab44d73c67ce489f67a523b

# https://forum.omz-software.com/topic/3221/request-token-not-found-from-dropbox-sync-in-pythonista-3/2

# YOU NEED TO INSERT YOUR APP KEY AND SECRET BELOW!
# Go to dropbox.com/developers/apps to create an app.

from __future__ import absolute_import
from __future__ import print_function
app_key = 'YOUR_APP_KEY'
app_secret = 'YOUR_APP_SECRET'

import webbrowser
import dropbox
import keychain

def get_access_token():
	access_token = keychain.get_password('dropboxv2', app_key)
	if access_token:
		return access_token
	auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
	authorize_url = auth_flow.start()
	print("1. Go to: " + authorize_url)
	print("2. Click \"Allow\" (you might have to log in first).")
	print("3. Copy the authorization code.")
	webbrowser.open(authorize_url, modal=True)
	auth_code = input("Enter the authorization code here: ").strip()
	try:
	    access_token, user_id = auth_flow.finish(auth_code)
	except Exception as e:
	    print('Error: %s' % (e,))
	    return
	keychain.set_password('dropboxv2', app_key, access_token)
	return access_token

def get_client():
	access_token = get_access_token()
	dbx = dropbox.Dropbox(access_token)
	return dbx

def main():
	# Demo if started run as a script...
	# Just print the account info to verify that the authentication worked:
	print('Getting account info...')
	dropbox_client = get_client()
	account_info = dropbox_client.users_get_current_account()
	print('linked account:', account_info)

if __name__ == '__main__':
    main()
