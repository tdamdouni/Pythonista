from __future__ import print_function
import webbrowser, os, pprint
# Include the Dropbox SDK libraries
#from dropbox import client, rest, session
import dropbox

# Configuration
TOKEN_FILENAME = 'DBToken'
# Get your app key and secret from the Dropbox developer website
APP_KEY = ''
APP_SECRET = ''

# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'dropbox'

# Program, do not edit from here

pp = pprint.PrettyPrinter(indent=4)

def configure_token(dropbox_session):
	if os.path.exists(TOKEN_FILENAME):
		token_file = open(TOKEN_FILENAME)
		token_key, token_secret = token_file.read().split('|')
		token_file.close()
		dropbox_session.set_token(token_key,token_secret)
	else:
		first_access()
	pass

def first_access():
	request_token = sess.obtain_request_token()
	url = sess.build_authorize_url(request_token)
	
	# Make the user sign in and authorize this token
	print("url:", url)
	print("Please visit this website and press the 'Allow' button, then hit 'Enter' here.")
	webbrowser.open(url)
	raw_input()
	# This will fail if the user didn't visit the above URL and hit 'Allow'
	access_token = sess.obtain_access_token(request_token)
	#save token file
	token_file = open(TOKEN_FILENAME,'w')
	token_file.write("%s|%s" % (access_token.key,access_token.secret) )
	token_file.close()
	pass

def main():
	sess = dropbox.session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
	configure_token(sess)
	client = dropbox.client.DropboxClient(sess)

	print("linked account: %s" % client.account_info()['display_name'])
	#pp.pprint (client.account_info())

	folder_metadata = client.metadata('/')
	#print "metadata"
	#pp.pprint(folder_metadata)

	for file in folder_metadata['contents']:
		if not os.path.exists(file['path']):
			print("Downloading file %s" % file['path'])
			try:
				out = open(file['path'][1:], 'w')
				file_content = client.get_file(file['path']).read()
				out.write(file_content)
			except:
				pass

	files = os.listdir(os.getcwd())
	choice = 'n'
	for file in files:
		if not os.path.isdir(file) and not file.startswith('.') and not file.startswith('desktop.ini'): # do not treat dirs as pythonista do not show this scripts
			found = client.search('/', file)
			if found:
				if not (choice == 'A' or choice == 'a'):
					print("File %s already on dropbox. Overwrite [Yes(y)|No(n)|All(a)|No to All}(na)] (Default No)" % file)
					choice = raw_input()
					if choice == 'na':
						break
				if choice == 'y' or choice == 'Y' or choice == 'A' or choice == 'a':
					print("Overwriting file %s" % file)
				##pp.pprint(client.search('/', file))
			else:
				#pp.pprint(client.metadata(file))
				print("Trying to upload %s" % file)
				client.put_file(file, open(file, 'r'), True)
				print("File %s uploaded to Dropbox" % file)


if __name__ == "__main__":
	main()
