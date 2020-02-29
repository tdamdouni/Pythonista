from __future__ import print_function
# https://gist.github.com/mlgill/8311046

# coding: utf-8
import dropbox, os, webbrowser
 
# A generic Dropbox module to create a token and login.
# Michelle L. Gill, 2014/01/06
 
# To use:
# import DropboxSetup
# sess, client = DropboxSetup.init(TOKEN_FILENAME, APP_KEY, APP_SECRET)
# TOKEN_DIRECTORY can be set to store tokens in a folder, set to "Tokens" by default
 
# requires a dropbox app key and secret, which can be created on dropbox's developer website
# most of this script was shamelessly copied from https://gist.github.com/ctaloi/4156185
 
def configure_token(sess, TOKEN_FILENAME, TOKEN_DIRECTORY):
	
	# if token directory is defined, make sure it ends in a backslash
	if ((TOKEN_DIRECTORY != '') and (TOKEN_DIRECTORY[-1] != os.sep)):
		TOKEN_DIRECTORY += os.sep
	
	# read token if it exists, otherwise create a new one
	if os.path.exists(TOKEN_DIRECTORY + TOKEN_FILENAME):
		token_file = open(TOKEN_DIRECTORY + TOKEN_FILENAME)
		token_key, token_secret = token_file.read().split('|')
		token_file.close()
		sess.set_token(token_key,token_secret)
	else:
		first_access(sess, TOKEN_FILENAME, TOKEN_DIRECTORY)
	return
 
 
def first_access(sess, TOKEN_FILENAME, TOKEN_DIRECTORY):
	request_token = sess.obtain_request_token()
	url = sess.build_authorize_url(request_token)
	
	# make the user sign in and authorize this token
	print("url:", url)
	print("Please visit this website and press the 'Allow' button, then hit 'Enter' here.")
	webbrowser.open(url)
	raw_input()
	
	# this will fail if the user didn't visit the above URL and hit 'Allow'
	access_token = sess.obtain_access_token(request_token)
	
	# create the token directory if necessary
	if TOKEN_DIRECTORY not in ['','.']:
		if not os.path.exists(TOKEN_DIRECTORY):
			os.mkdir(TOKEN_DIRECTORY)
		
	# save the token file
	token_file = open(TOKEN_DIRECTORY + TOKEN_FILENAME,'w')
	token_file.write("%s|%s" % (access_token.key,access_token.secret) )
	token_file.close()
	return
 
 
def init(TOKEN_FILENAME, APP_KEY, APP_SECRET, TOKEN_DIRECTORY='Tokens', ACCESS_TYPE='app_folder'):
	# create the Dropbox session and client for file interaction
	sess = dropbox.session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
	configure_token(sess, TOKEN_FILENAME, TOKEN_DIRECTORY)
	client = dropbox.client.DropboxClient(sess)
	
	return sess, client
 
if __name__ == "__main__":
	token_filename = raw_input('Enter token filename:').strip()
	app_key = raw_input('Enter app key:').strip()
	app_secret = raw_input('Enter app secret:').strip()
	sess, client = init(token_filename, app_key, app_secret)