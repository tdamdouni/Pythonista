from __future__ import print_function
# https://github.com/rmward/pythonista-dropbox-sync

import dropbox, os, webbrowser

# A generic Dropbox module to create a token and login.
# Michelle L. Gill, 2014/01/06

# To use:
# import dropboxsetup
# sess, client = dropboxsetup.init(TOKEN_FILENAME, APP_KEY, APP_SECRET)
# TOKEN_DIRECTORY can be set to store tokens in a folder, set to "Tokens" by default

# requires a dropbox app key and secret, which can be created on dropbox's developer website
# most of this script was shamelessly copied from https://gist.github.com/ctaloi/4156185
 
def configure_token(sess, TOKEN_FILENAME):
	
	# read token if it exists, otherwise create a new one
	if os.path.exists(TOKEN_FILENAME):
		token_file = open(TOKEN_FILENAME)
		token_key, token_secret = token_file.read().split('|')
		token_file.close()
		sess.set_token(token_key,token_secret)
	else:
		first_access(sess, TOKEN_FILENAME)
	return


def first_access(sess, TOKEN_FILENAME):
	request_token = sess.obtain_request_token()
	url = sess.build_authorize_url(request_token)
	
	# make the user sign in and authorize this token
	print("url:", url)
	print("Please visit this website and press the 'Allow' button, then hit 'Enter' here.")
	webbrowser.open(url)
	raw_input()
	
	# this will fail if the user didn't visit the above URL and hit 'Allow'
	access_token = sess.obtain_access_token(request_token)
	
	# save the token file
	token_file = open(TOKEN_FILENAME,'w')
	token_file.write("%s|%s" % (access_token.key,access_token.secret) )
	token_file.close()
	return


def init(TOKEN_FILENAME, APP_KEY, APP_SECRET, ACCESS_TYPE='app_folder'):
	# create the Dropbox session and client for file interaction
	sess = dropbox.session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
	configure_token(sess, TOKEN_FILENAME)
	client = dropbox.client.DropboxClient(sess)
	
	return sess, client

if __name__ == "__main__":
	token_filename = raw_input('Enter token filename:').strip()
	app_key = raw_input('Enter app key:').strip()
	app_secret = raw_input('Enter app secret:').strip()
	sess, client = init(token_filename, app_key, app_secret)
